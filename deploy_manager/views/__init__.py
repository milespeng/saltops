from .project import *
from .project_module import *

from django.template.defaultfilters import register
from django.utils.safestring import mark_safe
import better_exceptions
from deploy_manager.models.Project import JOB_SCRIPT_TYPE


@register.filter()
def jobscript_filter(value):
    for k in JOB_SCRIPT_TYPE:
        if k[0] == value:
            return k[1]


@register.filter()
def isrunning_filter(value):
    if value is True:
        return '运行中'
    else:
        return '未运行'
