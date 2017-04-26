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
