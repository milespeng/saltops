import logging
import uuid

import os

import yaml
from braces.views import *
from django.contrib.auth.mixins import *
from django.db import transaction
from django.utils.safestring import mark_safe
from django.urls import *
from django.views.generic import *

from cmdb.forms import ISPListFilterForm
from common.utils.logger_utils import LoggerUtils
from cmdb.models import Host, HostGroup
from common.pageutil import preparePage
from deploy_manager.forms import ProjectForm, ProjectVersionForm, ProjectListFilterForm
from deploy_manager.models import *
from saltjob.tasks import deploy_job_task, get_host_client_type, SALT_OPS_CONFIG
from saltops.settings import PER_PAGE, DEFAULT_LOGGER

import arrow
import zipfile

logger = logging.getLogger(DEFAULT_LOGGER)

listview_lazy_url = 'deploy_manager:project_list'
listview_template = 'deploy_manager/project_list.html'
formview_template = 'deploy_manager/project_form.html'


class ProjectView(LoginRequiredMixin,
                  OrderableListMixin,
                  ListView):
    model = Project
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['project_module', 'name', 'create_time', 'job_script_type',
                         'dev_monitor', 'ops_monitor']

    def get_queryset(self):
        result_list = Project.objects.all()
        name = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)
        if name:
            result_list = result_list.filter(name__contains=name)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = ProjectListFilterForm(self.request.GET)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'


class ProjectDeleteView(LoginRequiredMixin, JSONResponseMixin,
                        AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Project.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})


class ProjectVersionUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'deploy_manager/project_version_edit_form.html'
    form_class = ProjectVersionForm
    model = ProjectVersion

    def get_success_url(self):
        return '/frontend/deploy_manager/project_list/project_version/?pk=%s' % self.request.GET.get('pk')


class ProjectVersionDeleteView(LoginRequiredMixin, JSONResponseMixin,
                               AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            ProjectVersion.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})


class ProjectHostUnDeployActionView(LoginRequiredMixin, JSONResponseMixin,
                                    AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        projecthost = ProjectHost.objects.get(pk=int(self.request.GET.get('pk')))
        version = ProjectVersion.objects.get(pk=int(projecthost.project_version_id))
        job = DeployJob(project_version=version, job_name='卸载' + projecthost.host.host_name + ":" + version.name)
        job.save()
        hostlist = []
        hostlist.append(projecthost.host)
        # deployjob = deployTask.delay(job, 1, hostlist)
        projecthost.delete()
        return self.render_json_response({})


class ProjectHostDeployActionView(LoginRequiredMixin, JSONResponseMixin,
                                  AjaxResponseMixin, View):
    """
    业务部署，部署单台主机
    """

    @transaction.atomic
    def get_ajax(self, request, *args, **kwargs):
        projecthost = ProjectHost.objects.get(pk=int(self.request.GET.get('pk')),
                                              host=int(self.request.GET.get('host_id')))
        version = ProjectVersion.objects.get(pk=projecthost.project_version_id)

        is_success, deploy_result = deploy_job_task(projecthost.host.host_name,
                                                    version.name,
                                                    get_host_client_type(projecthost.host.enable_ssh))
        projecthost.deploy_states = 1 if is_success else 2
        projecthost.save()

        job = DeployJob(project_version=version,
                        job_name='部署' + projecthost.host.host_name + ":" + version.name)
        job.save()

        for k in deploy_result:
            deploy_job_detail = DeployJobDetail(host=projecthost.host,
                                                deploy_message=k['msg'],
                                                job=job,
                                                job_cmd=k['job_cmd'],
                                                duration=k['duration'],
                                                comment=k['comment'],
                                                is_success=k['is_success'])
            deploy_job_detail.save()

        result_list = [
            {
                'is_success': '部署成功' if is_success else '部署失败',
                'deploy_result': deploy_result,
                'host_name': projecthost.host.host_name
            }
        ]
        return self.render_json_response({
            'result_list': result_list,
        })


class ProjectHostStopActionView(LoginRequiredMixin, JSONResponseMixin,
                                AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        projecthost = ProjectHost.objects.get(pk=int(self.request.GET.get('pk')))
        version = ProjectVersion.objects.get(pk=(projecthost.project.current_version_id))
        job = DeployJob(project_version=version, job_name='停止' + projecthost.host.host_name + ":" + version.name)
        job.save()
        hostlist = []
        hostlist.append(projecthost.host)
        # deployjob = deployTask.delay(job, 4, hostlist)
        return self.render_json_response({})


class ProjectScanStateActionView(LoginRequiredMixin, JSONResponseMixin,
                                 AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        # scanProjectState()
        return self.render_json_response({})


class ProjectDeployActionView(LoginRequiredMixin, JSONResponseMixin,
                              AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        hosts = request.POST.get('hostids', '')
        project_pk = int(self.request.GET.get('pk'))
        obj = Project.objects.get(pk=project_pk)
        project_version_id = request.POST.get('version', '')
        # 记录下主机-业务-业务版本号的对应关系
        hosts_ids = hosts.split(',')
        for o in hosts_ids:
            ProjectHost(project=obj, host_id=int(o), project_version_id=project_version_id).save()
        #
        # # 添加部署任务记录
        # job = DeployJob(project_version=version, job_name='部署' + obj.name + ":" + version.name)
        # #TODO:使用事务改造，部署失败不要插入表里面
        # job.save()
        #
        # # 开始部署
        # deployTask.delay(job, 0)
        #
        # job_result = DeployJob.objects.get(pk=job.id)
        # jobDetails = DeployJobDetail.objects.filter(job=job_result)
        # job_detail_list = []
        #
        # # 整合数据结构
        # for o in jobDetails:
        #     target_obj = None
        #     for k in job_detail_list:
        #         if o.host.host_name == k['host_name']:
        #             target_obj = k
        #             break
        #
        #     is_successed_action = '执行成功'
        #     if o.is_success is False:
        #         is_successed_action = '执行失败'
        #     if target_obj is None:
        #         exec_rs = {'host_name': o.host.host_name, 'result': []}
        #         exec_rs['result'].append({
        #             'deploy_message': o.deploy_message,
        #             #            'job': o.job.job_name,
        #             'job_cmd': o.job_cmd,
        #             'start_time': o.start_time,
        #             'duration': str(o.duration),
        #             'stderr': o.stderr,
        #             'comment': o.comment,
        #             'is_success': is_successed_action,
        #             'id': o.id
        #         })
        #         job_detail_list.append(exec_rs)
        #     else:
        #         target_obj['result'].append({
        #             'deploy_message': o.deploy_message,
        #             #            'job': o.job.job_name,
        #             'job_cmd': o.job_cmd,
        #             'start_time': o.start_time,
        #             'duration': str(o.duration),
        #             'stderr': o.stderr,
        #             'comment': o.comment,
        #             'is_success': is_successed_action,
        #             'id': o.id
        #         })
        # # 判断任务是否执行成功
        # for o in job_detail_list:
        #     is_successed = True
        #     for k in o['result']:
        #         if k['is_success'] == '执行失败':
        #             is_successed = False
        #             break
        #     if is_successed is True:
        #         o['is_success'] = '执行成功'
        #     else:
        #         o['is_success'] = '执行失败'
        #
        # # 整体任务是否执行成功
        # deploy_status = '执行成功'
        # if job_result.deploy_status == 2:
        #     deploy_status = '执行失败'
        # result = {
        #     'deploy_status': deploy_status,
        #     'jobDetails': job_detail_list
        # }
        return self.render_json_response([])


class ProjectDeployView(LoginRequiredMixin, TemplateView):
    template_name = 'deploy_manager/project_deploy_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDeployView, self).get_context_data(**kwargs)
        # 获取版本关联的主机信息
        pk = self.request.GET.get('pk')
        project = Project.objects.get(pk=int(pk))
        project_version_obj = ProjectVersion.objects.filter(project=project).all()
        project_host = ProjectHost.objects.filter(project=project)
        host_list = list(Host.objects.all())
        for o in project_host:
            if o.host in host_list:
                host_list.remove(o.host)
        host_group_list = list(HostGroup.objects.all())
        context.update(locals())
        return context


class ProjectVersionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'deploy_manager/project_version_form.html'
    form_class = ProjectVersionForm
    model = ProjectVersion
    success_url = reverse_lazy(listview_lazy_url)

    def get_context_data(self, **kwargs):
        context = super(ProjectVersionCreateView, self).get_context_data(**kwargs)
        pk = self.request.GET.get('pk', '')
        if pk:
            project_versions = ProjectVersion.objects.filter(project_id=int(pk))
            context.update(locals())
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        project = Project.objects.get(pk=int(self.request.POST['pid']))
        obj = form.save()
        obj.project = project
        obj.save()
        # 解压SLS到
        f = zipfile.ZipFile(obj.files, 'r')
        for file in f.namelist():
            f.extract(file, SALT_OPS_CONFIG['package_path'])
        f.close()

        return super(ProjectVersionCreateView, self).form_valid(form)


class ProjectDeployHistoryView(ListView, LoginRequiredMixin):
    template_name = 'deploy_manager/project_deploy_history.html'
    context_object_name = 'result_list'
    paginate_by = PER_PAGE

    def get_queryset(self):
        result_list = DeployJob.objects.order_by('-create_time').filter(
            project_version__project=self.request.GET.get('pk'))
        return result_list

    def get_context_data(self, **kwargs):
        context = super(ProjectDeployHistoryView, self).get_context_data(**kwargs)
        result = []
        for deploy_job in context['result_list']:
            history = DeployJobDetail.objects.filter(job=deploy_job)
            result.append({
                "id": deploy_job.id,
                "create_time": deploy_job.create_time,
                "human_time": arrow.get(deploy_job.create_time).humanize(locale="zh"),
                "result_hist": history,
            })
        context['result_list'] = preparePage(self.request, result)
        return context
