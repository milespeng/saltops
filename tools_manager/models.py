from django.db import models

from cmdb.models import Host
from common.models import BaseModel


class ToolsTypes(BaseModel):
    name = models.CharField(max_length=255, verbose_name='类型名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "工具类型"
        verbose_name_plural = verbose_name


TOOL_RUN_TYPE = (
    (0, 'Salt脚本'),
    (1, 'Shell'),
    (2, 'PowerShell'),
    (3, 'Python')
)


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


class ToolsExecJob(BaseModel):
    tools = models.ForeignKey(ToolsScript, verbose_name='工具')
    hosts = models.ManyToManyField(Host, verbose_name='目标主机')
    param = models.TextField(verbose_name='执行参数', blank=True, null=True, default="")

    def __str__(self):
        return self.param

    class Meta:
        verbose_name = "工具执行"
        verbose_name_plural = verbose_name


class ToolsExecDetailHistory(BaseModel):
    tool_exec_history = models.ForeignKey(ToolsExecJob, blank=True, null=True)
    host = models.ForeignKey(Host, verbose_name='目标主机', blank=True, null=True)
    exec_result = models.TextField(verbose_name='执行结果', blank=True, null=True, default="")

    def __str__(self):
        return self.exec_result

    class Meta:
        verbose_name = "工具详细信息"
        verbose_name_plural = verbose_name
