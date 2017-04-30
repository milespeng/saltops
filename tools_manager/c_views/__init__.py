from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

from tools_manager.models import *


@register.filter()
def tools_count(value):
    obj = ToolsTypes.objects.get(pk=value)
    return mark_safe(
        '<a href="/frontend/cmdb/cabinet_list/?idc=&idc=%s">%s</a>' % (obj.id, obj.toolsscript_set.count()))
