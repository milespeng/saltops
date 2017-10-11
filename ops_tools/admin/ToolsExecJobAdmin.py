from django import forms
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from import_export.admin import ImportExportModelAdmin

from ops_tools.models import ToolsExecDetailHistory, ToolsExecJob


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
class ToolsExecJobAdmin(ImportExportModelAdmin):
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