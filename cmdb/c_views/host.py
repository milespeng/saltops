from http.client import HTTPResponse
import better_exceptions
from django.http import HttpResponse
from django.template.defaultfilters import register
from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.forms import ModelForm
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from cmdb.models import Cabinet, HostIP
from cmdb.models import Host
from cmdb.models import IDC
from cmdb.models import ISP
from cmdb.models import Rack
from cmdb.models.Host import MINION_STATUS
from common.pageutil import preparePage
from django.forms import *

from saltjob.tasks import scanHostJob


@require_http_methods(["GET"])
@gzip_page
@login_required
def scan_host_job(request):
    scanHostJob()
    return HttpResponse("")


def host_add_form_plugin(kwargs):
    return {'is_add': True}


def host_edit_form_plugin(kwargs):
    is_add = False
    obj = Host.objects.get(pk=int(kwargs['pk']))
    cabinet_list = Cabinet.objects.filter(idc=obj.idc)
    rack_list = Rack.objects.filter(cabinet__in=cabinet_list)
    host_ip_list = HostIP.objects.filter(host=obj)
    return {'rack_list': rack_list,
            'cabinet_list': cabinet_list,
            'is_add': is_add,
            'host_ip_list': host_ip_list
            }


# @require_http_methods(["POST"])
# @gzip_page
# @login_required
# def host_add_action(request, args):
#     module = __import__(args['modulename'])
#     instance = getattr(getattr(module, 'models'), args['modelname'])
#     form = modelform_factory(instance, fields='__all__')
#     form = form(request.POST)
#     if form.is_valid():
#         form.save()
#         return redirect(args['list_url'])
#     else:
#         return render(request, args['form_template_path'], locals())
