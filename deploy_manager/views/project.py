from braces.views import *
from django.contrib.auth.mixins import *
from django.utils.safestring import mark_safe
from django.urls import *
from django.views.generic import *

from saltjob.tasks import deployTask, loadProjectConfig
from cmdb.models import Host, HostGroup
from common.pageutil import preparePage
from deploy_manager.forms import ProjectForm, ProjectVersionForm
from deploy_manager.models import *
from saltops.settings import PER_PAGE

import arrow


class ProjectView(LoginRequiredMixin, ListView):
    model = Project
    paginate_by = PER_PAGE
    template_name = 'deploy_manager/project_list.html'
    context_object_name = 'result_list'

    def get_queryset(self):
        result_list = Project.objects.all()
        name = self.request.GET.get('name')
        if name:
            result_list = result_list.filter(name__contains=name)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', '')

        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'deploy_manager/project_form.html'
    success_url = reverse_lazy('deploy_manager:project_list')

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context['pre_project'] = Project.objects.all()
        return context

    def form_valid(self, form):
        obj = form.save()
        pre_project_list = self.request.POST.getlist('pre_project')
        if len(pre_project_list) > 0:
            for k in pre_project_list:
                PreProject(project=Project.objects.get(pk=k), current_project_id=obj.id).save()
        return super(ProjectCreateView, self).form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'deploy_manager/project_form.html'
    success_url = reverse_lazy('deploy_manager:project_list')
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context['pre_project'] = Project.objects.all()
        context['pre_project_selected'] = PreProject.objects.filter(current_project_id=self.object.id)
        return context

    def form_valid(self, form):
        obj = form.save()
        pre_project_list = self.request.POST.getlist('pre_project')
        PreProject.objects.filter(current_project_id=obj.id).delete()
        if len(pre_project_list) > 0:
            for k in pre_project_list:
                PreProject(project=Project.objects.get(pk=k), current_project_id=obj.id).save()
        return super(ProjectUpdateView, self).form_valid(form)


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


class ProjectHostGroupUnDeployActionView(LoginRequiredMixin, JSONResponseMixin,
                                         AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        hostgroup = ProjectHostGroup.objects.get(pk=int(self.request.GET.get('pk')))
        version = ProjectVersion.objects.get(is_default=True, project=hostgroup.project)
        job = DeployJob(project_version=version, job_name='卸载' + hostgroup.hostgroup.name + ":" + version.name)
        job.save()
        deployjob = deployTask.delay(job, True, list(Host.objects.filter(host_group=hostgroup.hostgroup)))
        hostgroup.delete()
        return self.render_json_response({})


class ProjectHostUnDeployActionView(LoginRequiredMixin, JSONResponseMixin,
                                    AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        projecthost = ProjectHost.objects.get(pk=int(self.request.GET.get('pk')))
        version = ProjectVersion.objects.get(is_default=True, project=projecthost.project)
        job = DeployJob(project_version=version, job_name='卸载' + projecthost.host.host_name + ":" + version.name)
        job.save()
        hostlist = []
        hostlist.append(projecthost.host)
        deployjob = deployTask.delay(job, True, hostlist)
        projecthost.delete()
        return self.render_json_response({})


def predeploy(project: Project, uninstall=False):
    """
    前置业务卸载功能暂不开放，有多重依赖的卸载关系需要考虑
    :param project: 
    :param uninstall: 
    :return: 
    """
    preprojects = PreProject.objects.filter(current_project_id=project.id)
    if len(preprojects) > 0:
        for k in preprojects:
            preproject_list = PreProject.objects.filter(current_project_id=k.project.id)
            if preproject_list.count() > 0:
                for o in preproject_list:
                    predeploy(Project.objects.get(pk=o.project.id), uninstall)
            else:
                pre_version = ProjectVersion.objects.get(project=k.project, is_default=True)
                job = DeployJob(project_version=pre_version,
                                job_name='部署' + k.project.name + ":" + pre_version.name)
                job.save()

                uninstall_host = []
                if uninstall is True:
                    uninstall_host_qs = ProjectHost.objects.filter(project=k.project)
                    for e in uninstall_host_qs:
                        uninstall_host.append(e)

                deployjob = deployTask.delay(job, uninstall, uninstall_host)


class ProjectDeployActionView(LoginRequiredMixin, JSONResponseMixin,
                              AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        # 目标主机
        hosts = request.POST.get('hostids', '')
        # 目标主机组
        host_groups = request.POST.get('hostgroup_ids', '')

        obj = Project.objects.get(pk=int(self.request.GET.get('pk')))
        version = obj.projectversion_set.get(is_default=True)

        if host_groups != '':
            host_groups_ids = host_groups.split(',')
            for o in host_groups_ids:
                ProjectHostGroup(project=obj, hostgroup_id=int(o)).save()
        if hosts != '':
            hosts_ids = hosts.split(',')
            for o in hosts_ids:
                ProjectHost(project=obj, host_id=int(o)).save()
        predeploy(obj)
        job = DeployJob(project_version=version, job_name='部署' + obj.name + ":" + version.name)
        job.save()
        deployjob = deployTask.delay(job)

        job_result = DeployJob.objects.get(pk=job.id)
        jobDetails = DeployJobDetail.objects.filter(job=job_result)
        job_detail_list = []

        # 整合数据结构
        for o in jobDetails:
            target_obj = None
            for k in job_detail_list:
                if o.host.host_name == k['host_name']:
                    target_obj = k
                    break

            is_successed_action = '执行成功'
            if o.is_success is False:
                is_successed_action = '执行失败'
            if target_obj is None:
                exec_rs = {'host_name': o.host.host_name, 'result': []}
                exec_rs['result'].append({
                    'deploy_message': o.deploy_message,
                    #            'job': o.job.job_name,
                    'job_cmd': o.job_cmd,
                    'start_time': o.start_time,
                    'duration': str(o.duration),
                    'stderr': o.stderr,
                    'comment': o.comment,
                    'is_success': is_successed_action
                })
                job_detail_list.append(exec_rs)
            else:
                target_obj['result'].append({
                    'deploy_message': o.deploy_message,
                    #            'job': o.job.job_name,
                    'job_cmd': o.job_cmd,
                    'start_time': o.start_time,
                    'duration': str(o.duration),
                    'stderr': o.stderr,
                    'comment': o.comment,
                    'is_success': is_successed_action
                })
        # 判断任务是否执行成功
        for o in job_detail_list:
            is_successed = True
            for k in o['result']:
                if k is False:
                    is_successed = False
                    break
            if is_successed is True:
                o['is_success'] = '执行成功'
            else:
                o['is_success'] = '执行失败'

        # 整体任务是否执行成功
        deploy_status = '执行成功'
        if job_result.deploy_status == 2:
            deploy_status = '执行失败'
        result = {
            'deploy_status': deploy_status,
            'jobDetails': job_detail_list
        }
        return self.render_json_response(result)


class ProjectDeployView(LoginRequiredMixin, TemplateView):
    template_name = 'deploy_manager/project_deploy_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDeployView, self).get_context_data(**kwargs)
        # 获取版本关联的主机信息
        pk = self.request.GET.get('pk')
        project = Project.objects.get(pk=int(pk))
        project_version_obj = ProjectVersion.objects.filter(project=project, is_default=True)[0]
        project_host = ProjectHost.objects.filter(project=project)
        project_host_group = ProjectHostGroup.objects.filter(project=project)
        host_list = list(Host.objects.all())
        for o in project_host:
            if o.host in host_list:
                host_list.remove(o.host)
        host_group_list = list(HostGroup.objects.all())
        for o in project_host_group:
            if o.hostgroup in host_group_list:
                host_group_list.remove(o.hostgroup)
        context.update(locals())
        return context


class ProjectVersionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'deploy_manager/project_version_form.html'
    form_class = ProjectVersionForm
    model = ProjectVersion
    success_url = reverse_lazy('deploy_manager:project_list')

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
        results = ProjectVersion.objects.filter(project=project)
        if 'is_default' in form.data and form.data['is_default'] == 'on':
            for k in results:
                k.is_default = False
                k.save()
            obj.project = project
            obj.is_default = True
            obj.save()
        else:
            obj = form.save()
            obj.project = project
            if len(results) == 0:
                obj.is_default = True
            else:
                obj.is_default = False
            obj.save()
        return super(ProjectVersionCreateView, self).form_valid(form)


class ProjectDeployHistoryView(TemplateView, LoginRequiredMixin):
    template_name = 'deploy_manager/project_deploy_history.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDeployHistoryView, self).get_context_data(**kwargs)
        result = []

        project = Project.objects.filter(id=self.request.GET.get('pk'))
        project_versions = ProjectVersion.objects.filter(project=project)

        for project_version in project_versions:
            obj = DeployJob.objects.order_by('-create_time').filter(project_version=project_version)
            for k in obj:
                history = DeployJobDetail.objects.filter(job=k)
                result.append({
                    "id": k.id,
                    "create_time": k.create_time,
                    "human_time": arrow.get(k.create_time).humanize(locale="zh"),
                    "result_hist": history,
                    # "success_count": len([x for x in history if x.err_msg == '']),
                    # "err_count": len([x for x in history if x.err_msg != ''])
                })
        context['result_list'] = preparePage(self.request, result)
        return context
