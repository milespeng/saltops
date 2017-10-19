from django.db import models

from common.constants import TOOL_RUN_TYPE
from common.models import BaseModel
from ops_polling.models import PollingJob
from ops_tools.models import ToolsTypes
from saltops2.settings import PACKAGE_PATH


class PollingScript(BaseModel):
    name = models.CharField(max_length=255, verbose_name='任务名称')
    tool_script = models.TextField(verbose_name='脚本', null=True)
    polling_job = models.ForeignKey(PollingJob, verbose_name='巡检任务')
    # tool_run_type = models.IntegerField(verbose_name='脚本类型', choices=(TOOL_RUN_TYPE), default=1)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "步骤"
        verbose_name_plural = verbose_name
