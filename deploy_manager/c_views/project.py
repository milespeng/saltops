from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
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
