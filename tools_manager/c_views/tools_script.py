from tools_manager.models import *
from tools_manager.models.ToolsScript import TOOL_RUN_TYPE
from collections import namedtuple
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, modelform_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods
import better_exceptions
from common.pageutil import preparePage


def tool_script_list_plugin():
    tools_types = ToolsTypes.objects.all()
    return {'tools_types': tools_types}


@require_http_methods(["GET"])
@gzip_page
@login_required
def tool_execute(request, pk):
    return render(request, 'frontend/tools_manager/tool_script_execute_form.html', locals(), RequestContext(request))
