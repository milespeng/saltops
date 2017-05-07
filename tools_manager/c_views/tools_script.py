import json
import re

import yaml
from django.utils.safestring import mark_safe

from cmdb.models import *
from saltjob.tasks import execTools
from tools_manager.models import *
from tools_manager.models.ToolsScript import TOOL_RUN_TYPE
from collections import namedtuple
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, modelform_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods
import better_exceptions
from common.pageutil import preparePage
import arrow


def tool_script_list_plugin():
    tools_types = ToolsTypes.objects.all()
    return {'tools_types': tools_types}


@require_http_methods(["GET"])
@gzip_page
@login_required
def tool_execute_history(request, pk):
    result = []
    obj = ToolsExecJob.objects.order_by('-create_time').filter(tools=pk)
    for k in obj:
        host = ""
        for h in k.hosts.all():
            host += h.host_name + "<br/>"

        history = ToolsExecDetailHistory.objects.filter(tool_exec_history=k)
        result.append({
            "id": k.id,
            "hosts_count": k.hosts.count(),
            "create_time": k.create_time,
            "human_time": arrow.get(k.create_time).humanize(locale="zh"),
            "hosts": mark_safe(host),
            "result_hist": history,
            "success_count": len([x for x in history if x.err_msg == '']),
            "err_count": len([x for x in history if x.err_msg != ''])
        })
        result_list = preparePage(request, result)
    return render(request, 'frontend/tools_manager/tool_script_execute_history.html', locals(), RequestContext(request))


@require_http_methods(["GET"])
@gzip_page
@login_required
def tool_execute(request, pk):
    hostgroup = HostGroup.objects.all()
    hosts = Host.objects.all()
    entity = ToolsScript.objects.get(pk=pk)
    params = re.findall('\${(.*?)}', entity.tool_script)
    param_list = []
    for obj in params:
        if len(obj.split(':')) == 2:
            param_dict = (obj.split(':')[0], obj.split(':')[1])
            param_list.append(param_dict)
    return render(request, 'frontend/tools_manager/tool_script_execute_form.html', locals(), RequestContext(request))


@require_http_methods(["POST"])
@gzip_page
@login_required
def tool_execute_action(request):
    hostids = request.POST['hostids']
    hostgroup_ids = request.POST['hostgroup_ids']
    obj = ToolsScript.objects.get(pk=request.POST['id'])
    params = re.findall('\${(.+?)}', obj.tool_script)
    param_obj = {}
    for entity in params:
        if ':' in entity:
            param_obj[entity.split(':')[1]] = request.POST[entity.split(':')[1]]
    if param_obj != "":
        yaml_str = yaml.dump(param_obj)
    hostlist = []
    if hostids != "":
        hostlist.extend(hostids.split(','))

    if hostgroup_ids != "":
        hosts = Host.objects.filter(host_group_id__in=hostgroup_ids.split(','))
        for k in hosts:
            hostlist.append(k.id)
    hostlist = list(set(hostlist))
    toolExecJob, exec_detail_list = execTools(obj, hostlist, yaml_str)
    # 把结果返回给前端展示
    result = []
    for k in exec_detail_list:
        result.append({
            'exec_result': k.exec_result,
            'err_msg': k.err_msg,
            'host': k.host.host_name,
        })
    return HttpResponse(json.dumps(result))
