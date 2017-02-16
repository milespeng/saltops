from django import forms
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect

from saltjob.tasks import execTools
from tools_manager.models import *


@admin.register(ToolsTypes)
class ToolsTypesAdmin(admin.ModelAdmin):
    list_display = ['name', 'script_count', 'create_time', 'update_time']
    search_fields = ['name']

    def script_count(self, obj):
        return '<a href="/admin/tools_manager/toolsscript/?q=&tools_type__id__exact=%s">%s</a>' % (
            obj.id, obj.toolsscript_set.count())

    script_count.short_description = '工具数量'
    script_count.allow_tags = True


@admin.register(ToolsScript)
class ToolsScriptAdmin(admin.ModelAdmin):
    list_display = ['name', 'tools_type', 'tool_run_type', 'comment', 'create_time', 'update_time', 'lastExecHistory']
    search_fields = ['name']
    list_filter = ['tools_type', 'tool_run_type']

    change_form_template = 'tools_script_change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['hostList'] = Host.objects.all()
        extra_context['is_edit'] = True
        return super(ToolsScriptAdmin, self).change_view(request, object_id=object_id, form_url=form_url,
                                                         extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if request.POST['action'] == '1':
            execTools(obj, request.POST.getlist('sls_hosts'), request.POST['txt_param'])
            self.message_user(request, "工具执行成功")
        else:
            obj.save()

    def lastExecHistory(self, obj):
        list = ToolsExecJob.objects.filter(tools=obj).order_by('-create_time')
        if len(list) > 0:
            obj = list[0]
            return '<a href="/admin/tools_manager/toolsexecjob/%s/change/">执行结果</a>' % obj.id
        else:
            return '-'

    lastExecHistory.allow_tags = True
    lastExecHistory.short_description = '执行结果'


class ToolsExecDetailHistoryInline(admin.StackedInline):
    model = ToolsExecDetailHistory
    fields = ['host', 'exec_result', 'err_msg']
    verbose_name = "执行记录"
    verbose_name_plural = "执行记录"
    readonly_fields = ['host', 'exec_result', 'err_msg']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ToolsExecJob)
class ToolsExecJobAdmin(admin.ModelAdmin):
    list_display = ['tools', 'param', 'create_time', 'update_time']
    search_fields = ['tools']
    list_filter = ['tools']
    readonly_fields = ['tools', 'hosts', 'param']
    inlines = [ToolsExecDetailHistoryInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = ('/static/js/ToolsExecJob.js',)
