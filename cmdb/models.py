# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models



class Host(models.Model):
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

    def __str__(self):
        return self.host_name

    class Meta:
        verbose_name = "主机"
        verbose_name_plural = verbose_name


class HostIP(models.Model):
    ip = models.CharField(max_length=255, blank=True, null=True, verbose_name="IP地址")
    host = models.ForeignKey(Host, default="", verbose_name="主机", blank=True, null=True, )

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "主机IP"
        verbose_name_plural = verbose_name
