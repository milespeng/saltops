import re

import yaml

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


def tool_script_list_plugin():
    tools_types = ToolsTypes.objects.all()
    return {'tools_types': tools_types}


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
    toolExecJob, exec_detail_list = execTools(obj, request.POST.getlist('sls_hosts'), yaml_str)
    # 把结果返回给前端展示
    return HttpResponse("")
