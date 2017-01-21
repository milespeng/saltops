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
                    'host', 'saltversion', 'num_gpus', 'system_serialnumber', 'cpu_model',
                    'os', 'mem_total', 'cpuarch', 'osarch']
    search_fields = ['host']
    inlines = [IPInline, ProjectInline]
