from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from cmdb.models import ISP


@admin.register(ISP)
class ISPAdmin(ImportExportModelAdmin):
    list_display = ['name', 'create_time', 'update_time']
    search_fields = ['name']
