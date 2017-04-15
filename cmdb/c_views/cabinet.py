from http.client import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.forms import ModelForm
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from cmdb.models import Cabinet
from cmdb.models import IDC
from cmdb.models import ISP
from common.pageutil import preparePage
from django.forms import *


class CabinetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CabinetForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Cabinet
        fields = '__all__'


@require_http_methods(["GET"])
@gzip_page
@login_required
def cabinet_list(request):
    idc = request.GET.get('idc', '')
    obj = Cabinet.objects.all()
    if idc != '':
        obj = obj.filter(idc=int(idc))
    result_list = preparePage(request, obj)
    idc_list = IDC.objects.all()
    return render(request, 'frontend/cmdb/cabinet_list.html', locals(), RequestContext(request))


@require_http_methods(["GET"])
@gzip_page
@login_required
def cabinet_delete_entity(request, pk):
    Cabinet.objects.filter(pk=pk).delete()
    return redirect('/frontend/cmdb/cabinet_list/')


@require_http_methods(["GET"])
@gzip_page
@login_required
def cabinet_add(request):
    title = '新增机架'
    action = '/frontend/cmdb/cabinet_list/cabinet_add_action/'
    form = CabinetForm()
    return render(request, 'frontend/cmdb/cabinet_form.html', locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def cabinet_add_action(request):
    form = CabinetForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/cabinet_list/')
    else:
        return render(request, 'frontend/cmdb/cabinet_form.html', locals())


@require_http_methods(["GET"])
@gzip_page
@login_required
def cabinet_edit(request, pk):
    title = '编辑机柜'
    action = '/frontend/cmdb/cabinet_list/%s/cabinet_edit_action/' % pk
    entity = get_object_or_404(Cabinet, pk=pk)
    form = CabinetForm(instance=entity)
    return render(request, 'frontend/cmdb/cabinet_form.html', locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def cabinet_edit_action(request, pk):
    entity = get_object_or_404(Cabinet, pk=pk)
    form = CabinetForm(request.POST, instance=entity)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/cabinet_list/')
    else:
        return render(request, 'frontend/cmdb/cabinet_form.html', locals())
