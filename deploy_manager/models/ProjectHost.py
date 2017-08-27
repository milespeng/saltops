from django.db import models
from cmdb.models import Host
from common.models import BaseModel
from deploy_manager.models.Project import Project

DEPLOY_STATUS = (
    (0, '未部署'),
    (1, '部署成功'),
    (2, '部署失败'),
)


class ProjectHost(BaseModel):
    host = models.ForeignKey(Host, verbose_name='主机')
    project = models.ForeignKey(Project, verbose_name='业务')
    is_running = models.BooleanField(null=False, blank=False, default=False, verbose_name='是否运行')
    project_version_id = models.TextField(default="", blank=True, null=True, verbose_name='已部署版本的ID')
    deploy_states = models.IntegerField(verbose_name='部署状态', choices=(DEPLOY_STATUS), default=0)

    def __str__(self):
        return self.host.host_name

    class Meta:
        verbose_name = "业务主机"
        verbose_name_plural = verbose_name
