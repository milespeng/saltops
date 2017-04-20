from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from cmdb.models.Cabinet import Cabinet
from cmdb.models.IDC import IDC
from common.models import BaseModel


class Rack(BaseModel):
    idc = models.ForeignKey(IDC, verbose_name='机房', blank=True, null=True)
    cabinet = models.ForeignKey(
        Cabinet,
        verbose_name="机柜",
        blank=True, null=True
    )
    name = models.CharField(max_length=30, unique=True, verbose_name="机架名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "机架"
        verbose_name_plural = verbose_name
        unique_together = (('idc', 'cabinet', 'name'),)
