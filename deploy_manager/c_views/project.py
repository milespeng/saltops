from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.shortcuts import redirect, render
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from deploy_manager.models import *


@require_http_methods(["POST"])
@gzip_page
@login_required
def project_add_action(request, args):
    form = modelform_factory(Project, fields='__all__')
    form = form(request.POST)
    if form.is_valid():
        return redirect(args['list_url'])
    else:
        return render(request, args['form_template_path'], locals())
