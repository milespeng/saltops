import json

from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods
import better_exceptions

from cmdb.models import Host, HostGroup
from deploy_manager.models import *
from saltjob.tasks import deployTask, loadProjectConfig


def add_form_plugin(args):
    pre_project = Project.objects.all()
    return {'pre_project': pre_project}


@require_http_methods(["GET"])
@gzip_page
@login_required
def project_version(request, pk):
    project_versions = ProjectVersion.objects.filter(project=Project.objects.get(pk=int(pk)))
    module = __import__('deploy_manager')
    instance = getattr(getattr(module, 'models'), 'ProjectVersion')
    form = modelform_factory(instance, fields='__all__')
    return render(request=request,
                  template_name='deploy_manager/project_version_form.html',
                  context=locals())


@require_http_methods(["GET"])
@gzip_page
@login_required
def delete_project_version(request, pk, args):
    ProjectVersion.objects.get(pk=int(pk)).delete()
    return HttpResponse('')


@require_http_methods(["GET"])
@gzip_page
@login_required
def project_deploy(request, pk, args):
    # 获取版本关联的主机信息
    project = Project.objects.get(pk=int(pk))
    project_version_obj = ProjectVersion.objects.filter(project=project, is_default=True)[0]
    project_host = ProjectHost.objects.filter(project=project)
    project_host_group = ProjectHostGroup.objects.filter(project=project)
    host_list = Host.objects.all()
    host_group_list = HostGroup.objects.all()
    return render(request=request,
                  template_name='deploy_manager/project_deploy_form.html',
                  context=locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def project_deploy_action(request, pk, args):
    hosts = request.POST.get('hostids', '')
    host_groups = request.POST.get('hostgroup_ids', '')
    obj = Project.objects.get(pk=pk)
    version = obj.projectversion_set.get(is_default=True)
    ProjectHostGroup.objects.filter(project=obj).delete()
    if host_groups != '':
        host_groups_ids = host_groups.split(',')
        for o in host_groups_ids:
            ProjectHostGroup(project=obj, hostgroup_id=int(o)).save()
    ProjectHost.objects.filter(project=obj).delete()
    if hosts != '':
        hosts_ids = hosts.split(',')
        for o in hosts_ids:
            ProjectHost(project=obj, host_id=int(o)).save()
    job = DeployJob(project_version=version, job_name='部署' + obj.name + ":" + version.name)
    job.save()
    deployjob = deployTask.delay(job)

    job_result = DeployJob.objects.get(pk=job.id)
    jobDetails = DeployJobDetail.objects.filter(job=job_result)
    job_detail_list = []
    for o in jobDetails:
        rs = {
            'host': o.host.host_name,
            'deploy_message': o.deploy_message,
            #            'job': o.job.job_name,
            'job_cmd': o.job_cmd,
            'start_time': o.start_time,
            #   'duration': o.duration,
            'stderr': o.stderr,
            'comment': o.comment,
            'is_success': o.is_success
        }
        job_detail_list.append(rs)
    deploy_status = '执行成功'
    if job_result.deploy_status == 2:
        deploy_status = '执行失败'
    result = {
        'deploy_status': deploy_status,
        'jobDetails': job_detail_list
    }
    # TODO:未完成
    result_list = []
    result_list.append(result)
    return HttpResponse(json.dumps(result_list))


@require_http_methods(["POST"])
@gzip_page
@login_required
def project_version_add_action(request, args):
    form = modelform_factory(ProjectVersion, fields='__all__')
    form = form(request.POST, request.FILES)
    project = Project.objects.get(pk=request.POST['id'])
    if form.is_valid():
        results = ProjectVersion.objects.filter(project=project)
        if 'is_default' in form.data and form.data['is_default'] == 'on':
            for k in results:
                k.is_default = False
                k.save()
            obj = form.save()
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
        return redirect(args['list_url'])
    else:
        return render(request, args['form_template_path'], locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def project_add_action(request, args):
    form = modelform_factory(Project, fields='__all__')
    form = form(request.POST)
    if form.is_valid():
        obj = form.save()
        pre_project_list = request.POST.getlist('pre_project')
        if len(pre_project_list) > 0:
            for k in pre_project_list:
                PreProject(project=Project.objects.get(pk=k), current_project_id=obj.id).save()
        return redirect(args['list_url'])
    else:
        return render(request, args['form_template_path'], locals())
