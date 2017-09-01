from .project import *
from .project_module import *

from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

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


@register.filter()
def deploy_states_filter(value):
    if value == 0:
        return '未部署'
    elif value == 1:
        return '部署成功'
    elif value == 2:
        return '部署失败'
    elif value == 3:
        return '启动成功'
    elif value == 4:
        return '启动失败'
    elif value == 5:
        return '暂停成功'
    elif value == 6:
        return '暂停失败'
    elif value == 7:
        return '卸载成功'
    elif value == 8:
        return '卸载失败'
    else:
        return ''


@register.filter()
def version_name_filter(value):
    return ProjectVersion.objects.get(pk=value).name
