from django.utils.safestring import mark_safe

from .idc import *
from .cabinet import *
from .rack import *
from .host_group import *
from .host import *


@register.filter()
def cabinet_count(value):
    obj = IDC.objects.get(pk=value)
    return mark_safe('<a href="/admin/cmdb/cabinet/?q=&idc=%s">%s</a>' % (obj.id, obj.cabinet_set.count()))
