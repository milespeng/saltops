from http.client import HTTPResponse

from django.db.models import Model
from django.forms import ModelForm
from django.shortcuts import render, render_to_response, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext

from cmdb.models import Cabinet
from cmdb.models import IDC
from cmdb.models import ISP
from common.pageutil import preparePage


def cabinet_list(request):
    idc = request.GET.get('idc', '')
    obj = Cabinet.objects.all()
    if idc != '':
        obj = obj.filter(idc=idc)
    result_list = preparePage(request, obj)
    idc_list = IDC.objects.all()
    return render(request, 'frontend/cmdb/cabinet_list.html', locals(), RequestContext(request))


def cabinet_delete_entity(request):
    pk = request.GET.get('id', '')
    if id != '':
        Cabinet.objects.filter(pk=pk).delete()
        return redirect('/frontend/cmdb/cabinet_list/')
    else:
        return redirect('/frontend/cmdb/cabinet_list/')


def cabinet_add(request):
    title = '新增机架'
    idc_list = IDC.objects.all()
    action = '/frontend/cmdb/cabinet_list/cabinet_add_action/'
    return render(request, 'frontend/cmdb/cabinet_form.html', locals())


def cabinet_add_action(request):
    obj = Cabinet(
        name=request.POST.get('name', ''),
        idc=IDC.objects.get(pk=request.POST.get('idc', '')),
    )
    obj.save()

    return redirect('/frontend/cmdb/cabinet_list/')


def cabinet_edit(request, pk):
    title = '编辑机柜'
    action = '/frontend/cmdb/cabinet_list/%s/cabinet_edit_action/' % pk
    entity = Cabinet.objects.get(pk=pk)
    idc_list = IDC.objects.all()
    return render(request, 'frontend/cmdb/cabinet_form.html', locals())


def cabinet_edit_action(request, pk):
    obj = Cabinet.objects.get(pk=pk)
    obj.name = request.POST.get('name', '')
    obj.idc = IDC.objects.get(pk=request.POST.get('idc', ''))
    obj.save()

    return redirect('/frontend/cmdb/cabinet_list/')
