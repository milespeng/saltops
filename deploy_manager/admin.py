# -*- coding: utf-8 -*-
import os
import threading
from uuid import uuid1

from django.contrib import admin
import salt.client
from django.urls import reverse
from mptt.admin import MPTTModelAdmin

from deploy_manager.models import *
import salt.runner
import salt.config
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class ProjectVersionInline(admin.TabularInline):
    model = ProjectVersion
    fields = ['name', 'is_default', 'files']
    verbose_name = '版本'
    verbose_name_plural = '版本'
    extra = 0


class HostInline(admin.TabularInline):
    model = Project.host.through
    fields = ['host']
    verbose_name = '主机'
    verbose_name_plural = '主机'
    extra = 0


@admin.register(ProjectModule)
class ProjectModuleAdmin(MPTTModelAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_module', 'name']
    search_fields = ['host']
    inlines = [ProjectVersionInline, HostInline]

    actions = ['deploydefaultAction', ]

    # 这里可以切换成自己的URL
    # def view_on_site(self, obj):
    #     url = reverse('person-detail', kwargs={'slug': obj.slug})
    #     return 'https://example.com' + url

    def deploydefaultAction(self, request, queryset):
        for obj in queryset:
            version = obj.projectversion_set.get(is_default=True)
            job = DeployJob(project_version=version, job_name='部署' + obj.name + ":" + version.name)
            job.save()
            thread = cmdThread(job)
            thread.start()
            self.message_user(request, "%s 个部署作业成功启动" % len(queryset))

    deploydefaultAction.short_description = "部署默认版本"


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

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class cmdThread(threading.Thread):
    def __init__(self, instances):
        threading.Thread.__init__(self)
        self.instances = instances

    def run(self):
        rc = salt.runner.RunnerClient(salt.config.master_config('/etc/salt/master'))
        project = self.instances.project_version.project
        hosts = project.host.all()
        uid = uuid1().__str__()
        scriptPath = PACKAGE_PATH + uid + ".sls"
        output = open(scriptPath, 'w')
        output.write(project.playbook)
        output.close()

        local = salt.client.LocalClient()
        result = local.cmd('*', 'state.sls', [uid])
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
                        job=self.instances
                    )
                    deployJobDetail.save()

        os.remove(scriptPath)
        self.instances.deploy_status = 1
        self.instances.save()


@admin.register(DeployJob)
class DeployJobAdmin(admin.ModelAdmin):
    list_display = ['job_name', 'project_version', 'deploy_status']
    readonly_fields = ['job_name', 'project_version', 'deploy_status']
    search_fields = ['job_name']
    list_filter = ['deploy_status']
    inlines = [DeployJobDetailInline]

    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = ('/static/js/DeployJobAdmin.js',)
