from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods
import better_exceptions
from deploy_manager.models import *


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
                  template_name='frontend/deploy_manager/project_version_form.html',
                  context=locals())


@require_http_methods(["GET"])
@gzip_page
@login_required
def delete_project_version(request, pk, args):
    ProjectVersion.objects.get(pk=int(pk)).delete()
    return HttpResponse('')


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
