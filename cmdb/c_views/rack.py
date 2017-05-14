import json
import better_exceptions
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Model
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from cmdb.models import *
from common.pageutil import preparePage
from django.forms import *


@require_http_methods(["GET"])
@gzip_page
@login_required
def load_cabinet_list(request, pk):
    data = serializers.serialize("json", Cabinet.objects.filter(idc=int(pk)))
    return HttpResponse(data)


@require_http_methods(["GET"])
@gzip_page
@login_required
def load_rack_list(request, idc_id, cabinet_id):
    data = serializers.serialize("json", Rack.objects.filter(idc=int(idc_id), cabinet=int(cabinet_id)))
    return HttpResponse(data)


def idc_list_plugin():
    idc = IDC.objects.all()
    return {'idc': idc}


def rack_edit_form_plugin(kwargs):
    is_add = False
    obj = Rack.objects.get(pk=int(kwargs['pk']))
    cabinet_list = Cabinet.objects.filter(idc=obj.idc)
    return {'cabinet_list': cabinet_list, 'is_add': is_add}


def rack_add_form_plugin(kwargs):
    is_add = True
    return {'is_add': is_add}
