from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin

from deploy_manager.models import *
from saltjob.tasks import deployTask


class ProjectModuleFilter(admin.SimpleListFilter):
    title = '上级业务模块'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        rs = set([c.parent for c in ProjectModule.objects.all()])
        v = set()
        for obj in rs:
            if obj is not None:
                v.add((obj.id, obj.name))
        return v

    def queryset(self, request, queryset):
        if 'parent' in request.GET:
            parentid = request.GET['parent']
            return queryset.filter(parent=parentid)
        else:
            return queryset.all()


@admin.register(ProjectModule)
class ProjectModuleAdmin(MPTTModelAdmin):
    list_display = ['name', 'parent', 'create_time', 'update_time']
    search_fields = ['name']
    list_filter = [ProjectModuleFilter, ]


class ProjectVersionInline(admin.StackedInline):
    model = ProjectVersion
    fields = ['name', 'sub_job_script_type', 'subplaybook', 'anti_install_playbook', 'extra_param', 'is_default',
              'files', ]
    verbose_name = '版本'
    verbose_name_plural = '版本'
    extra = 0

    class Media:
        js = (
            '/static/js/ProjectVersionInline.js',
        )


class HostInline(admin.TabularInline):
    model = Project.host.through
    fields = ['host']
    verbose_name = '主机'
    verbose_name_plural = '主机'
    extra = 0


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        exclude = ('project_module', 'host')


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    def construct_change_message(self, request, form, formsets, add=False):
        """
        删除业务后执行卸载脚本
        :param request:
        :param form:
        :param formsets:
        :param add:
        :return:
        """
        uninstall_list = []
        if formsets:
            for formset in formsets:
                for deleted_object in formset.deleted_objects:
                    uninstall_list.append(deleted_object.host)
        if len(uninstall_list) != 0:
            obj = form.instance
            version = obj.projectversion_set.get(is_default=True)
            job = DeployJob(project_version=version, job_name='卸载' + obj.name + ":" + version.name)
            job.save()
            deployTask.delay(job, True, uninstall_list)
            self.message_user(request, "卸载作业成功启动")
        return super(ProjectAdmin, self).construct_change_message(request, form, formsets, add)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<id>.+)/deploy_job/$',
                self.admin_site.admin_view(self.deploy_job),
                name='deploy_job',
            ),
        ]
        return custom_urls + urls

    list_display = ['project_module', 'name', 'job_script_type',
                    'create_time', 'update_time',
                    'deployMsg', 'extra_btn']
    search_fields = ['host']
    list_filter = ['job_script_type']
    inlines = [ProjectVersionInline, HostInline]
    list_display_links = ['project_module', 'deployMsg']
    actions = ['deploydefaultAction']
    resource_class = ProjectResource

    def extra_btn(self, obj):
        return format_html(
            '<a class="btn" href="{}">部署</a>',
            reverse('admin:deploy_job', args=[obj.pk]),
        )

    extra_btn.short_description = '操作'
    extra_btn.allow_tags = True

    def deploy_job(self, request, id):
        obj = Project.objects.get(pk=id)
        version = obj.projectversion_set.get(is_default=True)
        job = DeployJob(project_version=version, job_name='部署' + obj.name + ":" + version.name)
        job.save()
        deployTask.delay(job)
        self.message_user(request, "部署作业成功启动")
        return redirect('/admin/deploy_manager/project')

    def deployMsg(self, obj):
        try:
            return "<a href='/admin/deploy_manager/deployjob/%s/change/#/tab/inline_0/'>%s</a>" % (
                obj.projectversion_set.
                    get(is_default=True).deployjob_set.
                    order_by('-update_time').all()[0].id,
                dict(DEPLOY_STATUS)[obj.projectversion_set.
                    get(is_default=True).deployjob_set.
                    order_by('-update_time').all()[0].deploy_status])
        except Exception as e:
            return ""

    deployMsg.short_description = '部署状态'
    deployMsg.allow_tags = True

    def deploydefaultAction(self, request, queryset):
        for obj in queryset:
            version = obj.projectversion_set.get(is_default=True)
            job = DeployJob(project_version=version, job_name='部署' + obj.name + ":" + version.name)
            job.save()
            deployTask.delay(job)
            self.message_user(request, "%s 个部署作业成功启动" % len(queryset))

    deploydefaultAction.short_description = "部署默认版本"

    class Media:
        js = ('/static/js/Project.js',)


class DeployJobDetailInline(admin.StackedInline):
    model = DeployJobDetail
    fields = ['host', 'job_cmd', 'duration', 'deploy_message', 'stderr', 'comment', 'is_success']
    verbose_name = '作业详情'
    verbose_name_plural = '作业详情'
    extra = 0
    can_delete = False
    readonly_fields = ['host', 'job_cmd', 'duration', 'deploy_message', 'stderr',
                       'create_time', 'update_time', 'comment', 'is_success']
    ordering = ['-create_time']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DeployJob)
class DeployJobAdmin(admin.ModelAdmin):
    list_display = ['job_name', 'project_version', 'create_time', 'update_time', 'deploy_status']
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
