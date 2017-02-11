import requests
from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from cmdb.models import *
from deploy_manager.models import *
from saltjob.tasks import scanHostJob
from saltops.settings import SALT_CONN_TYPE, SALT_HTTP_URL


class IPInline(admin.TabularInline):
    model = HostIP
    fields = ['ip', 'ip_type']
    verbose_name = "IP"
    verbose_name_plural = "IP"
    extra = 0


class ProjectInline(admin.TabularInline):
    model = Project.host.through
    fields = ['project']
    verbose_name = '业务'
    verbose_name_plural = '业务'
    extra = 0


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ['host_name', 'kernel',
                    'host', 'rack', 'system_serialnumber',
                    'os', 'virtual', 'enable_ssh', 'minion_status', 'create_time', 'update_time']
    search_fields = ['host']
    list_filter = ['virtual', 'os_family', 'os', 'rack', 'minion_status']
    inlines = [IPInline, ProjectInline]

    def save_formset(self, request, form, formset, change):
        entity = form.save()
        formset.save()

        # 如果主机是SSH类型的，把SSH列表更新一遍
        if entity.enable_ssh is True:
            hosts = Host.objects.all()

            rosterString = ""
            for host in hosts:
                if host.enable_ssh is True:
                    rosterString += """

%s:
    host: %s
    user: %s
    passwd: %s
    sudo: %s
    tty: True

                """ % (host.host, host.host, host.ssh_username, host.ssh_password,
                       host.enable_ssh)

            if SALT_CONN_TYPE == 'http':
                requests.post(SALT_HTTP_URL + '/rouster', data={'content': rosterString})
            else:
                with open('/etc/salt/roster', 'w') as content:
                    content.write(rosterString)


class RackInline(NestedStackedInline):
    model = Rack
    fields = ['name']
    verbose_name = '机架'
    verbose_name_plural = '机架'
    extra = 0
    fk_name = 'cabinet'


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


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ['idc', 'name', 'rack_count', 'create_time', 'update_time']
    search_fields = ['name']
    fk_name = 'cabinet'
    list_filter = [IDCFilter]

    def rack_count(self, obj):
        return '<a href="/admin/cmdb/rack/?q=&cabinet__id__exact=%s">%s</a>' % (obj.id, obj.rack_set.count())

    rack_count.allow_tags = True
    rack_count.short_description = '机架数量'

    inlines = [RackInline]


class CabinetInline(NestedStackedInline):
    model = Cabinet
    fields = ['name']
    verbose_name = '机柜'
    verbose_name_plural = '机柜'
    extra = 0
    fk_name = 'idc'
    inlines = [RackInline]


@admin.register(IDC)
class IDCAdmin(NestedModelAdmin):
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


@admin.register(IDCLevel)
class IDCLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment', 'create_time', 'update_time']
    search_fields = ['name', 'comment']


@admin.register(ISP)
class ISPAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_time', 'update_time']
    search_fields = ['name']


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
class RackAdmin(admin.ModelAdmin):
    list_display = ['cabinet', 'name', 'create_time', 'update_time']
    search_fields = ['cabinet', 'name']
    list_filter = [CabinetFilter]
