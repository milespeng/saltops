from django.db import models

from cmdb.models import Host
from common.models import BaseModel
from ops_polling.models import PollingScript
from saltops2.settings import PACKAGE_PATH


class PollingJobHistory(BaseModel):
    polling_job = models.ForeignKey(PollingScript, verbose_name='巡检任务')
    hosts = models.ManyToManyField(Host, verbose_name='目标主机')
    report_template = models.FileField(upload_to=PACKAGE_PATH, verbose_name='巡检结果', null=True)

    def __str__(self):
        return self.param

    class Meta:
        verbose_name = "执行记录"
        verbose_name_plural = verbose_name
