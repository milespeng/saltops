from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

from tools_manager.models import *
from tools_manager.models.ToolsScript import TOOL_RUN_TYPE
from .tools_script import *


@register.filter()
def tools_count(value):
    obj = ToolsTypes.objects.get(pk=value)
    return mark_safe(
        '<a href="/frontend/cmdb/cabinet_list/?idc=&idc=%s">%s</a>' % (obj.id, obj.toolsscript_set.count()))


@register.filter()
def tools_type_filter(value):
    return TOOL_RUN_TYPE[value][1]
