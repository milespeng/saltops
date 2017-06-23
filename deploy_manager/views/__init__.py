from .project import *
from .project_module import *

from django.template.defaultfilters import register
from django.utils.safestring import mark_safe
import better_exceptions
from deploy_manager.models.Project import JOB_SCRIPT_TYPE


@register.filter()
def preproject_filter(value):
    pre_project = PreProject.objects.filter(current_project_id=value)
    content = ''
    if len(pre_project) == 0:
        return '无'
    else:
        for o in pre_project:
            content += o.project.name + '<br/>'

        return mark_safe(content)


@register.filter()
def jobscript_filter(value):
    for k in JOB_SCRIPT_TYPE:
        if k[0] == value:
            return k[1]


@register.filter()
def sub_jobscript_filter(value):
    project_version = ProjectVersion.objects.get(pk=value)

    if project_version.install_job_script_type == 100:
        project_ype_id = project_version.project.install_job_script_type
    else:
        project_ype_id = project_version.install_job_script_type
    for k in JOB_SCRIPT_TYPE:
        if k[0] == project_ype_id:
            return k[1]
