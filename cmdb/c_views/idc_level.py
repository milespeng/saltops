from http.client import HTTPResponse

from django.forms import *
from django.shortcuts import render, render_to_response, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext

from cmdb.models import IDCLevel
from common.pageutil import preparePage


class IDCLevelForm(ModelForm):
    class Meta:
        model = IDCLevel
        fields = '__all__'
        widgets = {
            'name': TextInput({'class': 'form-control'}),
            'comment': Textarea({'class': 'form-control'})
        }


def idc_level_list(request):
    idc_level = request.GET.get('idclevel', '')
    obj = IDCLevel.objects.all()
    if idc_level != '':
        obj = obj.filter(name=idc_level)
    result_list = preparePage(request, obj)
    return render(request, 'frontend/cmdb/idc_level_list.html', locals(), RequestContext(request))


def idc_level_delete_entity(request, pk):
    IDCLevel.objects.filter(pk=pk).delete()
    return redirect('/frontend/cmdb/idc_level_list/')


def idc_level_add(request):
    form = IDCLevelForm()
    title = '新增机房等级'
    action = '/frontend/cmdb/idc_level_list/idc_level_add_action/'
    return render(request, 'frontend/cmdb/idc_level_form.html', locals())


def idc_level_add_action(request):
    form = IDCLevelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/idc_level_list/')
    else:
        return render(request, 'frontend/cmdb/idc_level_form.html', locals())


def idc_level_edit(request, pk):
    title = '编辑机房等级'
    action = '/frontend/cmdb/idc_level_list/%s/idc_level_edit_action/' % pk
    form = IDCLevelForm(instance=IDCLevel.objects.get(pk=pk))
    return render(request, 'frontend/cmdb/idc_level_form.html', locals())


def idc_level_edit_action(request, pk):
    form = IDCLevelForm(request.POST, instance=IDCLevel.objects.get(pk=pk))
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/idc_level_list/')
    else:
        return render(request, 'frontend/cmdb/idc_level_form.html', locals())
