from django.shortcuts import render, redirect
from django.template import RequestContext
from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

from cmdb.models import IDC
from cmdb.models import IDCLevel
from cmdb.models import ISP
from common.pageutil import preparePage


def idc_list(request):
    @register.filter()
    def cabinet_count(value):
        obj = IDC.objects.get(pk=value)
        return mark_safe('<a href="/admin/cmdb/cabinet/?q=&idc=%s">%s</a>' % (obj.id, obj.cabinet_set.count()))

    isp = request.GET.get('isp', '')
    obj = IDC.objects.all()
    if isp != '':
        isp = int(isp)
        obj = obj.filter(operator=isp)
    result_list = preparePage(request, obj)

    isp_type = ISP.objects.all()
    return render(request, 'frontend/cmdb/idc_list.html', locals(), RequestContext(request))


def idc_add(request):
    title = '新增机房'
    action = '/frontend/cmdb/isp_list/idc_add_action/'
    isp_type = ISP.objects.all()
    idc_level = IDCLevel.objects.all()
    return render(request, 'frontend/cmdb/idc_form.html', locals())


def idc_add_action(request):
    obj = IDC(
        name=request.POST.get('name', ''),
        bandwidth=request.POST.get('bandwidth', ''),
        phone=request.POST.get('phone', ''),
        linkman=request.POST.get('linkman', ''),
        address=request.POST.get('address', ''),
        concat_email=request.POST.get('concat_email', ''),
        network=request.POST.get('network', ''),
        operator=ISP.objects.get(pk=request.POST.get('operator', '')),
        type=IDCLevel.objects.get(pk=request.POST.get('type', '')),
        comment=request.POST.get('comment', '')
    )
    obj.save()
    return redirect('/frontend/cmdb/idc_list/')


def idc_delete_entity(request):
    pk = request.GET.get('id', '')
    if id != '':
        IDC.objects.filter(pk=pk).delete()
        return redirect('/frontend/cmdb/idc_list/')
    else:
        return redirect('/frontend/cmdb/idc_list/')


def idc_edit(request, pk):
    title = '编辑机房'
    action = '/frontend/cmdb/idc_list/%s/idc_edit_action/' % pk
    entity = IDC.objects.get(pk=pk)
    isp_type = ISP.objects.all()
    idc_level = IDCLevel.objects.all()
    return render(request, 'frontend/cmdb/idc_form.html', locals())


def idc_edit_action(request, pk):
    obj = IDC.objects.get(pk=pk)
    obj.name = request.POST.get('name', '')
    obj.bandwidth = request.POST.get('bandwidth', '')
    obj.phone = request.POST.get('phone', '')
    obj.linkman = request.POST.get('linkman', '')
    obj.address = request.POST.get('address', '')
    obj.concat_email = request.POST.get('concat_email', '')
    obj.network = request.POST.get('network', '')
    obj.operator = ISP.objects.get(pk=request.POST.get('operator', ''))
    obj.type = IDCLevel.objects.get(pk=request.POST.get('type', ''))
    obj.comment = request.POST.get('comment', '')
    obj.save()
    return redirect('/frontend/cmdb/idc_list/')