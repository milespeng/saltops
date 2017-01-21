# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from cmdb.models import Host
from saltops.settings import PACKAGE_PATH


class Project(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="业务名称")
    host = models.ManyToManyField(Host, default="", verbose_name="主机",
                                  blank=True, through='ProjectHost')
    playbook = models.TextField(verbose_name='部署脚本', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "业务"
        verbose_name_plural = verbose_name


class ProjectVersion(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="版本名称")
    project = models.ForeignKey(Project, default="", verbose_name="业务名称", blank=True, null=True, )
    files = models.FileField(verbose_name='版本', blank=True, null=True, upload_to=PACKAGE_PATH+'files')

    def __str__(self):
        return self.project.__str__() + '---' + self.name

    class Meta:
        verbose_name = "版本信息"
        verbose_name_plural = verbose_name


class ProjectHost(models.Model):
    host = models.ForeignKey(Host, verbose_name='主机')
    project = models.ForeignKey(Project, verbose_name='业务')

    def __str__(self):
        return self.host.host_name

    class Meta:
        verbose_name = "业务主机"
        verbose_name_plural = verbose_name


class DeployJob(models.Model):
    project_version = models.ForeignKey(ProjectVersion, verbose_name='版本')
    job_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="作业名称")

    def __str__(self):
        return self.job_name

    class Meta:
        verbose_name = "部署作业"
        verbose_name_plural = verbose_name


class DeployJobDetail(models.Model):
    host = models.ForeignKey(Host, verbose_name='主机名')
    deploy_message = models.TextField(verbose_name='作业信息', blank=True, null=True)
    job = models.ForeignKey(DeployJob, verbose_name='作业名称', blank=True, null=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "部署详情"
        verbose_name_plural = verbose_name
