# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 07:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0002_auto_20170119_0717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='node_name',
            new_name='host',
        ),
        migrations.AddField(
            model_name='host',
            name='cpu_model',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='CPU\u578b\u53f7'),
        ),
        migrations.AddField(
            model_name='host',
            name='cpuarch',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='CPU\u67b6\u6784'),
        ),
        migrations.AddField(
            model_name='host',
            name='host_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4e3b\u673aDNS\u540d\u79f0'),
        ),
        migrations.AddField(
            model_name='host',
            name='kernel',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7cfb\u7edf\u5185\u6838'),
        ),
        migrations.AddField(
            model_name='host',
            name='kernel_release',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7cfb\u7edf\u5185\u6838\u7248\u672c'),
        ),
        migrations.AddField(
            model_name='host',
            name='mem_total',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u5185\u5b58\u5927\u5c0f'),
        ),
        migrations.AddField(
            model_name='host',
            name='num_gpus',
            field=models.IntegerField(blank=True, null=True, verbose_name='GPU\u6570\u91cf'),
        ),
        migrations.AddField(
            model_name='host',
            name='os',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf'),
        ),
        migrations.AddField(
            model_name='host',
            name='os_family',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7cfb\u7edf\u7c7b\u578b'),
        ),
        migrations.AddField(
            model_name='host',
            name='osarch',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7cfb\u7edf\u67b6\u6784'),
        ),
        migrations.AddField(
            model_name='host',
            name='osfinger',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7cfb\u7edf\u6307\u7eb9'),
        ),
        migrations.AddField(
            model_name='host',
            name='osrelease',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c'),
        ),
        migrations.AddField(
            model_name='host',
            name='productname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4ea7\u54c1\u540d\u79f0'),
        ),
        migrations.AddField(
            model_name='host',
            name='saltversion',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Salt\u7248\u672c'),
        ),
        migrations.AddField(
            model_name='host',
            name='system_serialnumber',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='SN\u53f7'),
        ),
        migrations.AddField(
            model_name='host',
            name='virtual',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u8bbe\u5907\u7c7b\u578b'),
        ),
    ]
