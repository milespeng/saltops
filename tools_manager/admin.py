from django import forms
from django.contrib import admin

from tools_manager.models import *


@admin.register(ToolsTypes)
class ToolsTypesAdmin(admin.ModelAdmin):
    list_display = ['name', 'script_count']
    search_fields = ['name']

    def script_count(self, obj):
        return obj.toolsscript_set.count()

        script_count.short_description = '工具数量'


class ToolsExecInline(admin.StackedInline):
    model = ToolsExecJob
    fields = ['hosts', 'param']
    verbose_name = "目标主机"
    verbose_name_plural = "目标主机"
    extra = 1
    max_num = 1


@admin.register(ToolsScript)
class ToolsScriptAdmin(admin.ModelAdmin):
    list_display = ['name', 'tools_type', 'tool_run_type', 'comment']
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
            print(12)

#
# @admin.register(ToolsExecJob)
# class ToolsScriptAdmin(admin.ModelAdmin):
#     list_display = ['tools', 'param']
#     search_fields = ['tools']
#     list_filter = ['tools']
