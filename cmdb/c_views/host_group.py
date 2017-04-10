from http.client import HTTPResponse
from django.template.defaultfilters import register
from django.db.models import Model
from django.forms import *
from django.shortcuts import render, render_to_response, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext

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


def hostgroup_delete_entity(request):
    pk = request.GET.get('id', '')
    if id != '':
        HostGroup.objects.filter(pk=pk).delete()
        return redirect('/frontend/cmdb/hostgroup_list/')
    else:
        return redirect('/frontend/cmdb/hostgroup_list/')


def hostgroup_add(request):
    title = '新增ISP'
    action = '/frontend/cmdb/hostgroup_list/hostgroup_add_action/'
    form = HostGroupForm()
    return render(request, 'frontend/cmdb/hostgroup_form.html', locals())


def hostgroup_add_action(request):
    form = HostGroupForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/hostgroup_list/')
    else:
        return render(request, 'frontend/cmdb/hostgroup_form.html', locals())


def hostgroup_edit(request, pk):
    title = '编辑ISP'
    action = '/frontend/cmdb/hostgroup_list/%s/hostgroup_edit_action/' % pk
    form = HostGroupForm(instance=HostGroup.objects.get(pk=pk))
    return render(request, 'frontend/cmdb/hostgroup_form.html', locals())


def hostgroup_edit_action(request, pk):
    form = HostGroupForm(request.POST, instance=HostGroup.objects.get(pk=pk))
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/hostgroup_list/')
    else:
        return render(request, 'frontend/cmdb/hostgroup_form.html', locals())
