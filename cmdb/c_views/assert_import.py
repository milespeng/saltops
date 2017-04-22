from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, modelform_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from common.pageutil import preparePage


@require_http_methods(["GET"])
@gzip_page
@login_required
def assert_import_index(request):
    return render(request, 'frontend/cmdb/assert_import_index.html', locals(), RequestContext(request))
