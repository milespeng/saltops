from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from nested_inline.admin import NestedStackedInline

from cmdb.filters import IDCFilter
from cmdb.models import Cabinet, Rack


class RackInline(NestedStackedInline):
    model = Rack
    fields = ['name']
    verbose_name = '机架'
    verbose_name_plural = '机架'
    extra = 0
    fk_name = 'cabinet'


@admin.register(Cabinet)
class CabinetAdmin(ImportExportModelAdmin):
    list_display = ['idc', 'name', 'rack_count', 'create_time', 'update_time']
    search_fields = ['name']
    fk_name = 'cabinet'
    list_filter = [IDCFilter]

    def rack_count(self, obj):
        return '<a href="/admin/cmdb/rack/?q=&cabinet__id__exact=%s">%s</a>' % (obj.id, obj.rack_set.count())

    rack_count.allow_tags = True
    rack_count.short_description = mark_safe('<a href="#">机架数量</a>')

    inlines = [RackInline]
