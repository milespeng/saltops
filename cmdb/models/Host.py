from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from cmdb.models import Rack, IDC, Cabinet
from common.constants import MINION_STATUS
from common.models import BaseModel


class Host(BaseModel):
    idc = models.ForeignKey(IDC, verbose_name='机房', blank=True, null=True)
    cabinet = ChainedForeignKey(
        Cabinet,
        verbose_name="机柜",
        chained_field="idc",
        chained_model_field="idc",
        show_all=False,
        auto_choose=True,
        sort=True, blank=True, null=True
    )
    rack = ChainedForeignKey(
        Rack,
        verbose_name="机架",
        chained_field="cabinet",
        chained_model_field="cabinet",
        show_all=False,
        auto_choose=True,
        sort=True, blank=True, null=True
    )
    host_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="主机DNS名称")
    enable_ssh = models.BooleanField(verbose_name='使用Salt-SSH', choices=((True, '启用'), (False, '禁用')), default=False)
    ssh_username = models.CharField(verbose_name='SSH用户名', max_length=255, blank=True, null=True, default="")
    ssh_password = models.CharField(verbose_name='SSH密码', max_length=255, blank=True, null=True, default="")
    enable_sudo = models.BooleanField(verbose_name='启用Sudo', choices=((True, '启用'), (False, '禁用')), default=False)
    kernel = models.CharField(max_length=255, blank=True, null=True, verbose_name="系统内核")
    kernel_release = models.CharField(max_length=255, blank=True, null=True, verbose_name="系统内核版本")
    virtual = models.CharField(max_length=255, blank=True, null=True, verbose_name="设备类型")
    host = models.CharField(max_length=255, blank=True, null=True, verbose_name="主机名")
    osrelease = models.CharField(max_length=255, blank=True, null=True, verbose_name="操作系统版本")
    saltversion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Salt版本")
    osfinger = models.CharField(max_length=255, blank=True, null=True, verbose_name="系统指纹")
    os_family = models.CharField(max_length=255, blank=True, null=True, verbose_name="系统类型")
    num_gpus = models.IntegerField(blank=True, null=True, verbose_name="GPU数量")
    system_serialnumber = models.CharField(max_length=255, blank=True, null=True, verbose_name="SN号")
    cpu_model = models.CharField(max_length=255, blank=True, null=True, verbose_name="CPU型号")
    productname = models.CharField(max_length=255, blank=True, null=True, verbose_name="产品名称")
    osarch = models.CharField(max_length=255, blank=True, null=True, verbose_name="系统架构")
    cpuarch = models.CharField(max_length=255, blank=True, null=True, verbose_name="CPU架构")
    os = models.CharField(max_length=255, blank=True, null=True, verbose_name="操作系统")
    mem_total = models.IntegerField(blank=True, null=True, verbose_name="内存大小")
    num_cpus = models.IntegerField(blank=True, null=True, verbose_name="CPU数量")
    minion_status = models.IntegerField(verbose_name='Minion状态', default=0,
                                        choices=MINION_STATUS)

    def __str__(self):
        return self.host_name

    class Meta:
        verbose_name = "主机"
        verbose_name_plural = verbose_name
