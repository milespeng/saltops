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
def host_list(request, args):
    kwargs = dict(filter(lambda x: x[1] != '', request.GET.dict().items()))
    if 'page' in kwargs:
        del kwargs['page']

    ip_filter = ''
    if 'ip_filter' in kwargs:
        ip_filter = kwargs['ip_filter']
        del kwargs['ip_filter']
    obj = Host.objects.filter(**kwargs)
    if ip_filter != '':
        host_ip_lists = HostIP.objects.filter(ip__contains=ip_filter)
        host_filter_list = []
        for k in host_ip_lists:
            host_filter_list.append(k.host)
        obj = obj.filter(host__in=host_filter_list)
    result_list = preparePage(request, obj)
    return render(request, args['template_path'], locals(), RequestContext(request))


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


@require_http_methods(["POST"])
@gzip_page
@login_required
def host_add_action(request, args):
    module = __import__(args['modulename'])
    instance = getattr(getattr(module, 'models'), args['modelname'])
    form = modelform_factory(instance, fields='__all__')
    form = form(request.POST)
    if form.is_valid():
        obj = form.save()
        host_ips = zip(request.POST.getlist('ip'), request.POST.getlist('ip_type'))
        for o in list(host_ips):
            HostIP(ip=o[0], ip_type=o[1], host=obj).save()
        return redirect(args['list_url'])
    else:
        return render(request, args['form_template_path'], locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def host_edit_action(request, pk, args):
    module = __import__(args['modulename'])
    instance = getattr(getattr(module, 'models'), args['modelname'])
    entity = get_object_or_404(instance, pk=pk)
    form = modelform_factory(instance, fields='__all__')
    form = form(request.POST, instance=entity)
    if form.is_valid():
        obj = form.save()
        HostIP.objects.filter(host=obj).delete()
        host_ips = zip(request.POST.getlist('ip'), request.POST.getlist('ip_type'))
        for o in list(host_ips):
            HostIP(ip=o[0], ip_type=o[1], host=obj).save()
        return redirect(args['list_url'])
    else:
        return render(request, args['form_template_path'], locals())
