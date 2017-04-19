from django.utils.safestring import mark_safe

from .idc import *
from .rack import *
from .host_group import *
from .host import *
from .cabinet import *


@register.filter()
def cabinet_count(value):
    obj = IDC.objects.get(pk=value)
    return mark_safe('<a href="/frontend/cmdb/cabinet_list/?idc=&idc=%s">%s</a>' % (obj.id, obj.cabinet_set.count()))
