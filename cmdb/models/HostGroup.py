from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from common.models import BaseModel


class HostGroup(MPTTModel, BaseModel):
    """
    主机组
    """
    parent = TreeForeignKey('self', verbose_name='上级分组',
                            null=True, blank=True, related_name='children', db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="主机组名称")

    class MPTTMeta:
        parent_attr = 'parent'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "主机组"
        verbose_name_plural = verbose_name
