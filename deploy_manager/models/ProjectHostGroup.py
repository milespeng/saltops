from django.db import models
from cmdb.models import Host, HostGroup
from common.models import BaseModel
from deploy_manager.models.Project import Project


class ProjectHostGroup(BaseModel):
    hostgroup = models.ForeignKey(HostGroup, verbose_name='主机组')
    project = models.ForeignKey(Project, verbose_name='业务')

    def __str__(self):
        return self.hostgroup.name

    class Meta:
        verbose_name = "业务主机组"
        verbose_name_plural = verbose_name
