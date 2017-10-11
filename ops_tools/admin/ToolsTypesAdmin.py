from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from ops_tools.models import ToolsTypes


@admin.register(ToolsTypes)
class ToolsTypesAdmin(ImportExportModelAdmin):
    list_display = ['name', 'script_count', 'create_time', 'update_time']
    search_fields = ['name']

    def script_count(self, obj):
        return '<a href="/admin/ops_tools/toolsscript/?q=&tools_type__id__exact=%s">%s</a>' % (
            obj.id, obj.toolsscript_set.count())

    script_count.short_description = '工具数量'
    script_count.allow_tags = True
