from django.template.defaultfilters import register

from cmdb.models.Host import MINION_STATUS
from .host_group import *
from .host import *
from .idclevel import *
from .isp import *
from .idc import *
from .cabinet import *
from .rack import *
from django.utils.safestring import mark_safe
from .assert_import import *
from cmdb.models.HostIP import IP_TYPE


@register.filter()
def cabinet_count(value):
    obj = IDC.objects.get(pk=value)
    return mark_safe('<a href="/frontend/cmdb/cabinet_list/?idc=&idc=%s">%s</a>' % (obj.id, obj.cabinet_set.count()))


@register.filter()
def parent_filter(value):
    if value is None:
        return '无'
    else:
        return value


@register.filter()
def enablessh_status_filter(value):
    if value is True:
        return '启用'
    else:
        return '禁用'


@register.filter()
def minion_status_filter(value):
    for k in MINION_STATUS:
        if k[0] == value:
            return k[1]


@register.filter()
def iptype_filter(value):
    for k in IP_TYPE:
        if k[0] == value:
            return k[1]


@register.filter()
def host_ip_filter(value):
    host_ips = HostIP.objects.filter(host=Host.objects.get(pk=value))
    content = ''
    for o in host_ips:
        for k in IP_TYPE:
            if k[0] == o.ip_type:
                content += '%s:%s<br/>' % (o.ip, k[1])

    return mark_safe(content)
