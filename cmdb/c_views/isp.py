from http.client import HTTPResponse

from django.shortcuts import render, render_to_response, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext

from cmdb.models import ISP
from common.pageutil import preparePage


def isp_list(request):
    name = request.GET.get('name', '')
    obj = ISP.objects.all()
    if name != '':
        obj = obj.filter(name=name)
    result_list = preparePage(request, obj)
    return render(request, 'frontend/cmdb/isp_list.html', locals(), RequestContext(request))


def isp_delete_entity(request):
    pk = request.GET.get('id', '')
    if id != '':
        ISP.objects.filter(pk=pk).delete()
        return redirect('/frontend/cmdb/isp_list/')
    else:
        return redirect('/frontend/cmdb/isp_list/')


def isp_add(request):
    title = '新增ISP'
    action = '/frontend/cmdb/isp_list/isp_add_action/'
    return render(request, 'frontend/cmdb/isp_form.html', locals())


def isp_add_action(request):
    obj = ISP(
        name=request.POST.get('name', ''),
    )
    obj.save()

    return redirect('/frontend/cmdb/isp_list/')


def isp_edit(request, pk):
    title = '编辑ISP'
    action = '/frontend/cmdb/isp_list/%s/isp_edit_action/' % pk
    entity = ISP.objects.get(pk=pk)
    return render(request, 'frontend/cmdb/isp_form.html', locals())


def isp_edit_action(request, pk):
    obj = ISP.objects.get(pk=pk)
    obj.name = request.POST.get('name', '')
    obj.comment = request.POST.get('comment', '')
    obj.save()

    return redirect('/frontend/cmdb/isp_list/')
