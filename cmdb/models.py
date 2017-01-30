# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from common.models import BaseModel


class ISP(BaseModel):
    name = models.CharField(max_length=255, verbose_name='名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ISP类型"
        verbose_name_plural = verbose_name


class IDCLevel(BaseModel):
    name = models.CharField(max_length=255, verbose_name='名称')
    comment = models.TextField(verbose_name='描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "机房等级"
        verbose_name_plural = verbose_name


class IDC(BaseModel):
    name = models.CharField(max_length=255, verbose_name='机房名称')
    bandwidth = models.CharField(max_length=255, blank=True, null=True, verbose_name='机房带宽')
    phone = models.CharField(max_length=255, verbose_name='联系电话')
    linkman = models.CharField(max_length=255, null=True, verbose_name='联系人')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="机房地址")
    concat_email = models.EmailField(verbose_name='联系邮箱', blank=True, null=True, default="")
    network = models.TextField(blank=True, null=True, verbose_name="IP地址段")
    create_time = models.DateField(auto_now=True, verbose_name='创建时间')
    operator = models.ForeignKey(ISP, verbose_name='ISP类型')
    type = models.ForeignKey(IDCLevel, verbose_name='机房类型')
    comment = models.TextField(blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "机房"
        verbose_name_plural = verbose_name


class Cabinet(BaseModel):
    idc = models.ForeignKey(IDC, verbose_name='机房')
    name = models.CharField(max_length=30, unique=True, verbose_name="机柜编号")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "机柜"
        verbose_name_plural = verbose_name


class Rack(BaseModel):
    cabinet = models.ForeignKey(Cabinet, verbose_name='机柜')
    name = models.CharField(max_length=30, unique=True, verbose_name="机架名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "机架"
        verbose_name_plural = verbose_name


class Host(BaseModel):
    host_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="主机DNS名称")
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
    rack = models.ForeignKey(Rack, verbose_name='机架', blank=True, null=True)

    def __str__(self):
        return self.host_name

    class Meta:
        verbose_name = "主机"
        verbose_name_plural = verbose_name


class HostIP(BaseModel):
    ip = models.CharField(max_length=255, blank=True, null=True, verbose_name="IP地址")
    host = models.ForeignKey(Host, default="", verbose_name="主机", blank=True, null=True, )

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "主机IP"
        verbose_name_plural = verbose_name
