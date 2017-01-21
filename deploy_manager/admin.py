# -*- coding: utf-8 -*-
import os
from uuid import uuid1

from django.contrib import admin
import salt.client
from deploy_manager.models import *
import salt.runner
import salt.config
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class ProjectVersionInline(admin.TabularInline):
    model = ProjectVersion
    fields = ['name', 'files']
    verbose_name = '版本'
    verbose_name_plural = '版本'
    extra = 0


class HostInline(admin.TabularInline):
    model = Project.host.through
    fields = ['host']
    verbose_name = '主机'
    verbose_name_plural = '主机'
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['host']
    inlines = [ProjectVersionInline, HostInline]


class DeployJobDetailInline(admin.StackedInline):
    model = DeployJobDetail
    fields = ['host', 'deploy_message']
    verbose_name = '作业详情'
    verbose_name_plural = '作业详情'
    extra = 0
    can_delete = False
    readonly_fields = ['host', 'deploy_message']

    def has_add_permission(self, request):
        return False

    def has_edit_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DeployJob)
class DeployJobAdmin(admin.ModelAdmin):
    list_display = ['job_name', 'project_version']
    search_fields = ['job_name']
    inlines = [DeployJobDetailInline]

    def save_formset(self, request, form, formset, change):
        instances = form.save(commit=False)
        project = instances.project_version.project
        hosts = project.host.all()
        formset.save()
        rc = salt.runner.RunnerClient(salt.config.master_config('/etc/salt/master'))

        uid = uuid1().__str__()
        scriptPath = PACKAGE_PATH + uid + ".sls"
        output = open(scriptPath, 'w')
        output.write(project.playbook)
        output.close()

        #暂时先用同步调用
        local = salt.client.LocalClient()
        result = local.cmd_async('*', 'state.sls', [uid])
        for master in result:
            if isinstance(result[master], dict):
                for cmd in result[master]:
                    targetHost = Host.objects.get(host_name=master)
                    msg = ""
                    if "stdout" in result[master][cmd]['changes']:
                        msg = result[master][cmd]['changes']["stdout"]
                    deployJobDetail = DeployJobDetail(
                        host=targetHost,
                        deploy_message=msg,
                        job=instances
                    )
                    deployJobDetail.save()

        os.remove(scriptPath)
