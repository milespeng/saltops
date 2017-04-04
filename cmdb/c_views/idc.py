from django.shortcuts import render
from django.template import RequestContext
from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

from cmdb.models import IDC
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
