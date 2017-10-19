from django.db import models

from cmdb.models import Host
from common.models import BaseModel
from saltops2.settings import PACKAGE_PATH


class PollingJob(BaseModel):
    name = models.CharField(max_length=255, verbose_name='巡检名称')
    report_template = models.FileField(upload_to=PACKAGE_PATH, null=True, verbose_name='巡检模板')
    polling_hosts = models.ManyToManyField(Host, verbose_name='巡检主机', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "巡检任务"
        verbose_name_plural = verbose_name
