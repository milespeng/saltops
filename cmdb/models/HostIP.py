from django.db import models

from cmdb.models import Host
from common.constants import IP_TYPE
from common.models import BaseModel


class HostIP(BaseModel):
    ip = models.CharField(max_length=255, blank=True, null=True, verbose_name="IP地址")
    host = models.ForeignKey(Host, default="", verbose_name="主机", blank=True, null=True, )
    ip_type = models.IntegerField(verbose_name='IP类型', blank=True, choices=IP_TYPE, default=100)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "主机IP"
        verbose_name_plural = verbose_name
