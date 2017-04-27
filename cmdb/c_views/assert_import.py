import os
from cmdb.models import *
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.forms import ModelForm, modelform_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods
import xlrd
from common.pageutil import preparePage
from django.core.files.storage import default_storage

from saltops import settings


@require_http_methods(["GET"])
@gzip_page
@login_required
def assert_import_index(request):
    return render(request, 'frontend/cmdb/assert_import_index.html', locals(), RequestContext(request))


@require_http_methods(["POST"])
@gzip_page
@login_required
def upload_file(request):
    assert_file = request.FILES.get("file", None)
    wb = xlrd.open_workbook(filename=None, file_contents=assert_file.read())
    # 读取机房等级信息
    idc_level_table = wb.sheets()[0]
    for i in range(1, idc_level_table.nrows):
        row = idc_level_table.row_values(i)
        if len(IDCLevel.objects.filter(name=row[0])) == 0:
            IDCLevel(name=row[0], comment=row[1]).save()

    # 读取ISP信息
    isp_table = wb.sheets()[1]
    for i in range(1, isp_table.nrows):
        row = isp_table.row_values(i)
        if len(ISP.objects.filter(name=row[0])) == 0:
            ISP(name=row[0]).save()

    # 读取机房信息
    idc_table = wb.sheets()[2]
    for i in range(1, idc_table):
        row = isp_table.row_values(i)
        if len(IDC.objects.filter(name=row[0])) == 0:
            try:
                IDC(name=row[0], bandwidth=row[1],
                    phone=row[2], linkman=row[3],
                    address=row[4], concat_email=row[5],
                    network=row[6], operator=ISP.objects.get(name=row[7]),
                    type=IDCLevel.objects.get(name=row[8]), comment=row[9]).save()
            except Exception as e:
                pass

    # 机柜
    for i in range(1, wb.sheets()[3]):
        row = wb.sheets()[3].row_values(i)
        if len(Cabinet.objects.filter(name=row[1])) == 0:
            try:
                Cabinet(idc=IDC.objects.get(name=row[0]), name=row[1]).save()
            except Exception as e:
                pass

    # 机架
    for i in range(1, wb.sheets()[4]):
        row = wb.sheets()[4].row_values(i)
        if len(Rack.objects.filter(name=row[1])) == 0:
            try:
                Rack(idc=IDC.objects.get(name=row[0]),
                     cabinet=Cabinet.objects.get(name=row[1]),
                     name=row[2]).save()
            except Exception as e:
                pass

    # 主机组
    for i in range(1, wb.sheets()[5]):
        row = wb.sheets()[5].row_values(i)
        if len(HostGroup.objects.filter(name=row[0])) == 0:
            try:
                if row[0] == "":
                    HostGroup(name=row[1]).save()
                else:
                    HostGroup(parent=HostGroup.objects.get(name=row[0]), name=row[1]).save()
            except Exception as e:
                pass

    # 主机
    for i in range(1, wb.sheets()[6]):
        row = wb.sheets()[6].row_values(i)
        if len(Host.objects.filter(name=row[0])) == 0:
            try:
                enable_sudo = False
                if row[7] != '0':
                    enable_sudo = True
                Host(host_group=HostGroup.objects.get(name=row[0]),
                     host=row[1],
                     idc=IDC.objects.get(name=row[2]),
                     cabinet=Cabinet.objects.get(name=row[3]),
                     rack=Rack.objects.get(name=row[4]),
                     enable_ssh=True,
                     ssh_username=row[5],
                     ssh_password=row[6],
                     enable_sudo=enable_sudo)
            except Exception as e:
                pass
    return HttpResponse("")
