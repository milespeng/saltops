from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from cmdb.models import IDCLevel


@admin.register(IDCLevel)
class IDCLevelAdmin(ImportExportModelAdmin):
    list_display = ['name', 'comment', 'create_time', 'update_time']
    search_fields = ['name', 'comment']