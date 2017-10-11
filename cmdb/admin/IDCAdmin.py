from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from cmdb.models import IDC, Cabinet, Rack


class RackInline(NestedStackedInline):
    model = Rack
    fields = ['name']
    verbose_name = '机架'
    verbose_name_plural = '机架'
    extra = 0
    fk_name = 'cabinet'


class CabinetInline(NestedStackedInline):
    model = Cabinet
    fields = ['name']
    verbose_name = '机柜'
    verbose_name_plural = '机柜'
    extra = 0
    fk_name = 'idc'
    inlines = [RackInline]


@admin.register(IDC)
class IDCAdmin(ImportExportModelAdmin, NestedModelAdmin):
    list_display = ['name', 'type', 'phone',
                    'linkman', 'address',
                    'operator', 'concat_email', 'cabinet_count', 'create_time', 'update_time']
    search_fields = ['name']
    inlines = [CabinetInline]
    list_filter = ['type']

    def cabinet_count(self, obj):
        return '<a href="/admin/cmdb/cabinet/?q=&idc=%s">%s</a>' % (obj.id, obj.cabinet_set.count())

    cabinet_count.short_description = '机柜数量'
    cabinet_count.allow_tags = True
