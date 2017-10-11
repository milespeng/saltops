from django.contrib import admin

from cmdb.models import IDC


class IDCFilter(admin.SimpleListFilter):
    title = '机房'
    parameter_name = 'idc'

    def lookups(self, request, model_admin):
        rs = set([c for c in IDC.objects.all()])
        v = set()
        for obj in rs:
            if obj is not None:
                v.add((obj.id, obj.name))
        return v

    def queryset(self, request, queryset):
        if 'idc' in request.GET:
            idc = request.GET['idc']
            return queryset.filter(idc=idc)
        else:
            return queryset.all()