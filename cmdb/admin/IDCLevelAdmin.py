from django.contrib import admin

from cmdb.models import IDCLevel


@admin.register(IDCLevel)
class IDCLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment', 'create_time', 'update_time']
    search_fields = ['name', 'comment']