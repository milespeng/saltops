import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Model
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from cmdb.models import *
from common.pageutil import preparePage
from django.forms import *


class RackForm(ModelForm):
    class Meta:
        model = Rack
        fields = '__all__'
        widgets = {
            'idc': Select({'class': 'form-control'}),
            'cabinet': Select({'class': 'form-control'}),
            'name': TextInput({'class': 'form-control'}),
        }


@require_http_methods(["GET"])
@gzip_page
@login_required
def load_cabinet_list(request, pk):
    data = serializers.serialize("json", Cabinet.objects.filter(idc=int(pk)))
    return HttpResponse(data)


@require_http_methods(["GET"])
@gzip_page
@login_required
def load_rack_list(request, idc_id, cabinet_id):
    data = serializers.serialize("json", Rack.objects.filter(idc=int(idc_id), cabinet=int(cabinet_id)))
    return HttpResponse(data)


@require_http_methods(["GET"])
@gzip_page
@login_required
def rack_list(request):
    cabinet = request.GET.get('cabinet', '')
    obj = Rack.objects.all()
    if cabinet != '':
        obj = obj.filter(cabinet=int(cabinet))
    result_list = preparePage(request, obj)
    cabinet_list = Cabinet.objects.all()
    return render(request, 'frontend/cmdb/rack_list.html', locals(), RequestContext(request))


@require_http_methods(["GET"])
@gzip_page
@login_required
def rack_delete_entity(request, pk):
    Rack.objects.filter(pk=pk).delete()
    return redirect('/frontend/cmdb/rack_list/')


@require_http_methods(["GET"])
@gzip_page
@login_required
def rack_add(request):
    is_add = True
    title = '新增机架'
    action = '/frontend/cmdb/rack_list/rack_add_action/'
    form = RackForm()
    return render(request, 'frontend/cmdb/rack_form.html', locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def rack_add_action(request):
    form = RackForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/rack_list/')
    else:
        return render(request, 'frontend/cmdb/rack_form.html', locals())


@require_http_methods(["GET"])
@gzip_page
@login_required
def rack_edit(request, pk):
    title = '编辑机架'
    action = '/frontend/cmdb/rack_list/%s/rack_edit_action/' % pk
    obj = get_object_or_404(Rack, pk=pk)
    form = RackForm(instance=obj)
    cabinet_list = Cabinet.objects.filter(idc=obj.idc)
    is_add = False
    return render(request, 'frontend/cmdb/rack_form.html', locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def rack_edit_action(request, pk):
    entity = get_object_or_404(Rack, pk=pk)
    form = RackForm(request.POST, instance=entity)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/rack_list/')
    else:
        return render(request, 'frontend/cmdb/rack_form.html', locals())
