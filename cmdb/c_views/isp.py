from http.client import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.forms import *
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from cmdb.models import ISP
from common.pageutil import preparePage


class ISPForm(ModelForm):
    class Meta:
        model = ISP
        fields = '__all__'
        widgets = {
            'name': TextInput({'class': 'form-control'})
        }


@require_http_methods(["GET"])
@gzip_page
@login_required
def isp_list(request):
    name = request.GET.get('name', '')
    obj = ISP.objects.all()
    if name != '':
        obj = obj.filter(name=name)
    result_list = preparePage(request, obj)

    return render(request, 'frontend/cmdb/isp_list.html', locals(), RequestContext(request))


@require_http_methods(["GET"])
@gzip_page
@login_required
def isp_delete_entity(request, pk):
    ISP.objects.filter(pk=pk).delete()
    return redirect('/frontend/cmdb/isp_list/')


@require_http_methods(["GET"])
@gzip_page
@login_required
def isp_add(request):
    title = '新增ISP'
    action = '/frontend/cmdb/isp_list/isp_add_action/'
    form = ISPForm()
    return render(request, 'frontend/cmdb/isp_form.html', locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def isp_add_action(request):
    form = ISPForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/isp_list/')
    else:
        return render(request, 'frontend/cmdb/isp_form.html', locals())


@require_http_methods(["GET"])
@gzip_page
@login_required
def isp_edit(request, pk):
    title = '编辑ISP'
    action = '/frontend/cmdb/isp_list/%s/isp_edit_action/' % pk
    entity = get_object_or_404(ISP, pk=pk)
    form = ISPForm(instance=entity)
    return render(request, 'frontend/cmdb/isp_form.html', locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def isp_edit_action(request, pk):
    entity = get_object_or_404(ISP, pk=pk)
    form = ISPForm(request.POST, instance=entity)
    if form.is_valid():
        form.save()
        return redirect('/frontend/cmdb/isp_list/')
    else:
        return render(request, 'frontend/cmdb/isp_form.html', locals())
