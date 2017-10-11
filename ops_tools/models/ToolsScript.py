from django.db import models

from common.constants import TOOL_RUN_TYPE
from common.models import BaseModel
from ops_tools.models import ToolsTypes


class ToolsScript(BaseModel):
    name = models.CharField(max_length=255, verbose_name='工具名称')
    tool_script = models.TextField(verbose_name='脚本')
    tools_type = models.ForeignKey(ToolsTypes, verbose_name='工具类型')
    tool_run_type = models.IntegerField(verbose_name='脚本类型', choices=(TOOL_RUN_TYPE), default=0)
    comment = models.TextField(verbose_name='工具说明', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "工具"
        verbose_name_plural = verbose_name
