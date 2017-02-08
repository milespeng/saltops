from django.contrib import admin
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


class ProjectVersionInline(admin.TabularInline):
    model = ProjectVersion
    fields = ['name', 'sub_job_script_type', 'subplaybook', 'is_default', 'files', ]
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
    list_display = ['project_module', 'name', 'job_script_type',
                    'create_time', 'update_time',
                    'deployMsg']
    search_fields = ['host']
    list_filter = ['job_script_type']
    inlines = [ProjectVersionInline, HostInline]
    list_display_links = ['project_module', 'deployMsg', ]
    actions = ['deploydefaultAction']
    resource_class = ProjectResource

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

    # def save_formset(self, request, form, formset, change):
    #     instances = form.save(commit=False)
    #     formset.save()

    # 这里可以切换成自己的URL
    # def view_on_site(self, obj):
    #     url = reverse('person-detail', kwargs={'slug': obj.slug})
    #     return 'https://example.com' + url

    def deploydefaultAction(self, request, queryset):
        for obj in queryset:
            version = obj.projectversion_set.get(is_default=True)
            job = DeployJob(project_version=version, job_name='部署' + obj.name + ":" + version.name)
            job.save()
            deployTask.delay(job)
            self.message_user(request, "%s 个部署作业成功启动" % len(queryset))

    deploydefaultAction.short_description = "部署默认版本"

    # class Media:
    # js = ('/static/js/Project.js',)


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
