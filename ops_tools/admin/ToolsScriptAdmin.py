import re

import yaml
from django.contrib import admin
from django.http import HttpResponseRedirect
from import_export.admin import ImportExportModelAdmin

from cmdb.models import Host
from crontasks.tasks.exec_tools_job import execTools
from ops_tools.models import ToolsScript, ToolsExecJob


@admin.register(ToolsScript)
class ToolsScriptAdmin(ImportExportModelAdmin):
    list_display = ['name', 'tools_type', 'tool_run_type', 'comment', 'create_time', 'update_time', 'lastExecHistory']
    search_fields = ['name']
    list_filter = ['tools_type', 'tool_run_type']

    # 设置编辑页面
    change_form_template = 'tools_script_change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['hostList'] = Host.objects.all()
        extra_context['is_edit'] = True
        obj = ToolsScript.objects.get(pk=object_id)
        params = re.findall('\${(.*?)}', obj.tool_script)
        param_list = []
        for obj in params:
            if len(obj.split(':')) == 2:
                param_dict = (obj.split(':')[0], obj.split(':')[1])
                param_list.append(param_dict)
        extra_context['param'] = param_list
        return super(ToolsScriptAdmin, self).change_view(request, object_id=object_id, form_url=form_url,
                                                         extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        obj.save()
        if request.POST['action'] == '1':
            params = re.findall('\${(.+?)}', obj.tool_script)
            param_obj = {}
            for entity in params:
                if ':' in entity:
                    param_obj[entity.split(':')[1]] = request.POST[entity.split(':')[1]]
            if param_obj != "":
                yaml_str = yaml.dump(param_obj)
            toolExecJob, exec_detail_list = execTools(obj, request.POST.getlist('sls_hosts'), yaml_str)
            self.message_user(request, "工具执行成功")
            self.toolExecJob = toolExecJob

    def response_post_save_change(self, request, obj):
        if request.POST['action'] == '1':
            return HttpResponseRedirect(
                '/admin/ops_tools/toolsexecjob/%s/change/#/tab/inline_0/' % self.toolExecJob.id)
        else:
            return super(ToolsScriptAdmin, self).changelist_view(request)

    def lastExecHistory(self, obj):
        list = ToolsExecJob.objects.filter(tools=obj).order_by('-create_time')
        if len(list) > 0:
            obj = list[0]
            return '<a href="/admin/ops_tools/toolsexecjob/%s/change/">执行结果</a>' % obj.id
        else:
            return '-'

    lastExecHistory.allow_tags = True
    lastExecHistory.short_description = '执行结果'
