# -*- coding: utf-8 -*-
from django.contrib import admin

from cmdb.models import *
from deploy_manager.models import *


class IPInline(admin.TabularInline):
    model = HostIP
    fields = ['ip']
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
    list_display = ['host_name', 'kernel', 'kernel_release',
                    'host', 'rack', 'saltversion', 'num_gpus', 'system_serialnumber', 'cpu_model',
                    'os', 'mem_total', 'cpuarch', 'osarch']
    search_fields = ['host']
    inlines = [IPInline, ProjectInline]
    # fieldsets = (
    #     ('基础信息', {
    #         'fields': ('host_name', 'kernel', 'kernel_release','virtual',
    #                    'host','osrelease','osfinger','os_family','num_gpus','system_serialnumber')
    #     }),
    #     ('Agent信息', {
    #         'fields': ('saltversion',)
    #     }),
    # )


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ['idc', 'name']
    search_fields = ['name']


@admin.register(IDC)
class IDCAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'phone',
                    'linkman', 'address',
                    'operator', 'concat_email', 'create_time']
    search_fields = ['name']


@admin.register(IDCLevel)
class IDCLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment']
    search_fields = ['name', 'comment']


@admin.register(ISP)
class ISPAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['cabinet', 'name']
    search_fields = ['cabinet', 'name']
