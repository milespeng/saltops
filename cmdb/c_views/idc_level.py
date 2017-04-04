from http.client import HTTPResponse

from django.shortcuts import render, render_to_response, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext

from cmdb.models import IDCLevel
from common.pageutil import preparePage


def idc_level_list(request):
    idc_level = request.GET.get('idclevel', '')
    obj = IDCLevel.objects.all()
    if idc_level != '':
        obj = obj.filter(name=idc_level)
    result_list = preparePage(request, obj)
    return render(request, 'frontend/cmdb/idc_level_list.html', locals(), RequestContext(request))


def idc_level_delete_entity(request):
    pk = request.GET.get('id', '')
    if id != '':
        IDCLevel.objects.filter(pk=pk).delete()
        return redirect('/frontend/cmdb/idc_level_list/')
    else:
        return redirect('/frontend/cmdb/idc_level_list/')


def idc_level_add(request):
    title = '新增机房等级'
    action = '/frontend/cmdb/idc_level_list/idc_level_add_action/'
    return render(request, 'frontend/cmdb/idc_level_form.html', locals())


def idc_level_add_action(request):
    obj = IDCLevel(
        name=request.POST.get('name', ''),
        comment=request.POST.get('comment', ''),
    )
    obj.save()

    return redirect('/frontend/cmdb/idc_level_list/')
