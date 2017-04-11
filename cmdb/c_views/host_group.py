from http.client import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import register
from django.db.models import Model
from django.forms import *
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from cmdb.models import *
from common.pageutil import preparePage


class HostGroupForm(ModelForm):
    class Meta:
        model = HostGroup
        fields = '__all__'
        widgets = {
            'parent': Select({'class': 'form-control'}),
            'name': TextInput({'class': 'form-control'})
        }


@require_http_methods(["GET"])
@gzip_page
@login_required
def hostgroup_list(request):
    @register.filter()
    def hostgroup_parent_filter(value):
        if value is None:
            return '无'
        else:
            return value

    obj = HostGroup.objects.all()
    result_list = preparePage(request, obj)
    return render(request, 'frontend/cmdb/hostgroup_list.html', locals(), RequestContext(request))


@require_http_methods(["GET"])
@gzip_page
@login_required
def hostgroup_delete_entity(request, pk):
    HostGroup.objects.filter(pk=pk).delete()
    return redirect('/frontend/cmdb/hostgroup_list/')


@require_http_methods(["GET"])
@gzip_page
@login_required
def hostgroup_add(request):
    title = '新增ISP'
    action = '/frontend/cmdb/hostgroup_list/hostgroup_add_action/'
    form = HostGroupForm()
    return render(request, 'frontend/cmdb/hostgroup_form.html', locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def hostgroup_add_action(request):
    form = HostGroupForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/hostgroup_list/')
    else:
        return render(request, 'frontend/cmdb/hostgroup_form.html', locals())


@require_http_methods(["GET"])
@gzip_page
@login_required
def hostgroup_edit(request, pk):
    title = '编辑ISP'
    action = '/frontend/cmdb/hostgroup_list/%s/hostgroup_edit_action/' % pk
    entity = get_object_or_404(HostGroup, pk=pk)
    form = HostGroupForm(instance=entity)
    return render(request, 'frontend/cmdb/hostgroup_form.html', locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def hostgroup_edit_action(request, pk):
    entity = get_object_or_404(HostGroup, pk=pk)
    form = HostGroupForm(request.POST, instance=entity)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/hostgroup_list/')
    else:
        return render(request, 'frontend/cmdb/hostgroup_form.html', locals())
