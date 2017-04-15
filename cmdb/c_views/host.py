from http.client import HTTPResponse
from django.template.defaultfilters import register
from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.forms import ModelForm
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from cmdb.models import Host
from cmdb.models import IDC
from cmdb.models import ISP
from cmdb.models.Host import MINION_STATUS
from common.pageutil import preparePage
from django.forms import *


class HostForm(ModelForm):
    class Meta:
        model = Host
        fields = '__all__'
        widgets = {
            'host_group': Select({'class': 'form-control'}),
            'host_name': TextInput({'class': 'form-control'}),
            'kernel': TextInput({'class': 'form-control'}),
            'kernel_release': TextInput({'class': 'form-control'}),
            'virtual': TextInput({'class': 'form-control'}),
            'host': TextInput({'class': 'form-control'}),
            'osrelease': TextInput({'class': 'form-control'}),
            'saltversion': TextInput({'class': 'form-control'}),
            'osfinger': TextInput({'class': 'form-control'}),
            'os_family': TextInput({'class': 'form-control'}),
            'num_gpus': TextInput({'class': 'form-control'}),
            'system_serialnumber': TextInput({'class': 'form-control'}),
            'cpu_model': TextInput({'class': 'form-control'}),
            'productname': TextInput({'class': 'form-control'}),
            'osarch': TextInput({'class': 'form-control'}),
            'cpuarch': TextInput({'class': 'form-control'}),
            'os': TextInput({'class': 'form-control'}),
            'mem_total': TextInput({'class': 'form-control'}),
            'num_cpus': TextInput({'class': 'form-control'}),
            'idc': Select({'class': 'form-control'}),
            'cabinet': Select({'class': 'form-control'}),
            'rack': Select({'class': 'form-control'}),
            'minion_status': Select({'class': 'form-control'}),
            'enable_ssh': Select({'class': 'form-control'}),
            'ssh_username': TextInput({'class': 'form-control'}),
            'ssh_password': TextInput({'class': 'form-control'}),
            'enable_sudo': Select({'class': 'form-control'}),

        }


@require_http_methods(["GET"])
@gzip_page
@login_required
def host_list(request):
    @register.filter()
    def minion_status_filter(value):
        for k in MINION_STATUS:
            if k[0] == value:
                return k[1]

    @register.filter()
    def enablessh_status_filter(value):
        if value is True:
            return '启用'
        else:
            return '禁用'

    idc = request.GET.get('idc', '')
    obj = Host.objects.all()
    if idc != '':
        obj = obj.filter(idc=int(idc))
    result_list = preparePage(request, obj)
    idc_list = IDC.objects.all()
    return render(request, 'frontend/cmdb/host_list.html', locals(), RequestContext(request))


@require_http_methods(["GET"])
@gzip_page
@login_required
def host_delete_entity(request, pk):
    Host.objects.filter(pk=pk).delete()
    return redirect('/frontend/cmdb/host_list/')


@require_http_methods(["GET"])
@gzip_page
@login_required
def host_add(request):
    title = '新增主机'
    action = '/frontend/cmdb/host_list/host_add_action/'
    form = HostForm()
    return render(request, 'frontend/cmdb/host_form.html', locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def host_add_action(request):
    form = HostForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/host_list/')
    else:
        return render(request, 'frontend/cmdb/host_form.html', locals())


@require_http_methods(["GET"])
@gzip_page
@login_required
def host_edit(request, pk):
    title = '编辑主机'
    action = '/frontend/cmdb/host_list/%s/host_edit_action/' % pk
    entity = get_object_or_404(Host, pk=pk)
    form = HostForm(instance=entity)
    return render(request, 'frontend/cmdb/host_form.html', locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def host_edit_action(request, pk):
    entity = get_object_or_404(Host, pk=pk)
    form = HostForm(request.POST, instance=entity)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/host_list/')
    else:
        return render(request, 'frontend/cmdb/host_form.html', locals())
