from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from deploy_manager.models import ProjectModule


def project_module_list_plugin():
    project_module = ProjectModule.objects.filter(parent=None).all()
    return {'project_module': project_module}


