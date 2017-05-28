import re

import arrow
import yaml
from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.utils.safestring import mark_safe
from django.views.generic import *

from cmdb.models import HostGroup, Host
from common.pageutil import preparePage
from saltjob.tasks import execTools
from saltops.settings import PER_PAGE
from tools_manager.forms import *
from tools_manager.models import *


class ToolsScriptView(LoginRequiredMixin, ListView):
    model = ToolsScript
    paginate_by = PER_PAGE
    template_name = 'tools_manager/tools_script_list.html'
    context_object_name = 'result_list'


class ToolsScriptCreateView(LoginRequiredMixin, CreateView):
    model = ToolsScript
    form_class = ToolsScriptForm
    template_name = 'tools_manager/tools_script_form.html'
    success_url = reverse_lazy('tools_manager:tools_script_list')


class ToolsScriptUpdateView(LoginRequiredMixin, UpdateView):
    model = ToolsScript
    form_class = ToolsScriptForm
    template_name = 'tools_manager/tools_script_form.html'
    success_url = reverse_lazy('tools_manager:tools_script_list')


class ToolsScriptDeleteView(LoginRequiredMixin, JSONResponseMixin,
                            AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            ToolsScript.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})


class ToolExecuteHistoryView(TemplateView, LoginRequiredMixin):
    template_name = 'tools_manager/tool_script_execute_history.html'

    def get_context_data(self, **kwargs):
        context = super(ToolExecuteHistoryView, self).get_context_data(**kwargs)
        result = []
        obj = ToolsExecJob.objects.order_by('-create_time').filter(tools=self.request.GET.get('pk'))
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
            context['result_list'] = preparePage(self.request, result)
            return context


class ToolExecuteView(TemplateView, LoginRequiredMixin):
    template_name = 'tools_manager/tool_script_execute_form.html'

    def get_context_data(self, **kwargs):
        context = super(ToolExecuteView, self).get_context_data(**kwargs)
        context['hostgroup'] = HostGroup.objects.all()
        context['hosts'] = Host.objects.all()
        pk = int(self.request.GET.get('pk'))
        entity = ToolsScript.objects.get(pk=pk)
        context['pk'] = pk
        context['entity'] = entity
        params = re.findall('\${(.*?)}', entity.tool_script)
        param_list = []
        for obj in params:
            if len(obj.split(':')) == 2:
                param_dict = (obj.split(':')[0], obj.split(':')[1])
                param_list.append(param_dict)
        context['param_list'] = param_list
        return context


class ToolExecuteActionView(LoginRequiredMixin, JSONResponseMixin,
                            AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        hostids = request.POST['hostids']
        hostgroup_ids = request.POST['hostgroup_ids']
        obj = ToolsScript.objects.get(pk=int(request.POST.get('id')))
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
        return self.render_json_response(result)
