from django import forms
from django.contrib import admin

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


class ToolsExecInline(admin.StackedInline):
    model = ToolsExecJob
    fields = ['hosts', 'param']
    verbose_name = "目标主机"
    verbose_name_plural = "目标主机"
    extra = 1
    max_num = 1


@admin.register(ToolsScript)
class ToolsScriptAdmin(admin.ModelAdmin):
    list_display = ['name', 'tools_type', 'tool_run_type', 'comment', 'create_time', 'update_time']
    search_fields = ['name']
    list_filter = ['tools_type', 'tool_run_type']
    inlines = [ToolsExecInline, ]

    class Media:
        js = ('/static/js/ToolsScriptAdmin.js',)

    def save_formset(self, request, form, formset, change):
        entity = form.save()
        formset.save()

        # TODO:执行脚本
        if request.POST['action'] == '1':
            execTools(entity)


class ToolsExecDetailHistoryInline(admin.StackedInline):
    model = ToolsExecDetailHistory
    fields = ['host', 'exec_result']
    verbose_name = "执行记录"
    verbose_name_plural = "执行记录"
    readonly_fields = ['host', 'exec_result']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ToolsExecJob)
class ToolsExecJobAdmin(admin.ModelAdmin):
    list_display = ['tools', 'param']
    search_fields = ['tools']
    list_filter = ['tools']
    readonly_fields = ['tools', 'hosts', 'param', 'create_time', 'update_time']
    inlines = [ToolsExecDetailHistoryInline, ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = ('/static/js/ToolsExecJob.js',)
