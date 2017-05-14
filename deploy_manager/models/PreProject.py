from django.contrib.auth.models import User
from django.db import models

from cmdb.models import Host
from common.models import BaseModel
from deploy_manager.models import Project
from deploy_manager.models.ProjectModule import ProjectModule


class PreProject(BaseModel):
    project = models.ForeignKey(Project, null=True, blank=True, verbose_name='前置业务')
    current_project_id = models.IntegerField(null=True)

    def __str__(self):
        return self.project.name

    class Meta:
        verbose_name = "前置业务"
        verbose_name_plural = verbose_name
