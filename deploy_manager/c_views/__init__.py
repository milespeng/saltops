from .project_module import *
from .project import *
from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

from deploy_manager.models.Project import JOB_SCRIPT_TYPE


@register.filter()
def jobscript_filter(value):
    for k in JOB_SCRIPT_TYPE:
        if k[0] == value:
            return k[1]
