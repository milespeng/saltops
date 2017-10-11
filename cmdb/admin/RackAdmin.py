from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin

from cmdb.models import Rack, Cabinet


class CabinetFilter(admin.SimpleListFilter):
    title = '机柜'
    parameter_name = 'cabinet'

    def lookups(self, request, model_admin):
        rs = set([c for c in Cabinet.objects.all()])
        v = set()
        for obj in rs:
            if obj is not None:
                v.add((obj.id, obj.name))
        return v

    def queryset(self, request, queryset):
        if 'cabinet' in request.GET:
            cabinet = request.GET['cabinet']
            return queryset.filter(cabinet=cabinet)
        else:
            return queryset.all()


@admin.register(Rack)
class RackAdmin(ImportExportModelAdmin):
    list_display = ['idc_column', 'cabinet', 'name', 'create_time', 'update_time']
    search_fields = ['cabinet', 'name']
    list_filter = [CabinetFilter]

    def idc_column(self, obj):
        return obj.cabinet.idc.name

    idc_column.allow_tags = True
    idc_column.short_description = mark_safe('<a href="#">机房</a>')
    list_display_links = ('cabinet',)
