from django.forms import *
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

from cmdb.models import IDC
from cmdb.models import IDCLevel
from cmdb.models import ISP
from common.pageutil import preparePage


class IDCForm(ModelForm):
    class Meta:
        model = IDC
        fields = '__all__'
        widgets = {
            'name': TextInput({'class': 'form-control'}),
            'bandwidth': TextInput({'class': 'form-control'}),
            'phone': TextInput({'class': 'form-control'}),
            'linkman': TextInput({'class': 'form-control'}),
            'address': TextInput({'class': 'form-control'}),
            'concat_email': TextInput({'class': 'form-control'}),
            'network': TextInput({'class': 'form-control'}),
            'operator': Select({'class': 'form-control'}),
            'type': Select({'class': 'form-control'}),
            'comment': Textarea({'class': 'form-control'}),
        }


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
    action = '/frontend/cmdb/idc_list/idc_add_action/'
    form = IDCForm()
    return render(request, 'frontend/cmdb/idc_form.html', locals())


def idc_add_action(request):
    form = IDCForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/idc_list/')
    else:
        return render(request, 'frontend/cmdb/idc_form.html', locals())


def idc_delete_entity(request, pk):
    IDC.objects.filter(pk=pk).delete()
    return redirect('/frontend/cmdb/idc_list/')


def idc_edit(request, pk):
    title = '编辑机房'
    action = '/frontend/cmdb/idc_list/%s/idc_edit_action/' % pk
    form = IDCForm(instance=IDC.objects.get(pk=pk))
    return render(request, 'frontend/cmdb/idc_form.html', locals())


def idc_edit_action(request, pk):
    form = IDCForm(request.POST, instance=IDC.objects.get(pk=pk))
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/idc_list/')
    else:
        return render(request, 'frontend/cmdb/idc_form.html', locals())
