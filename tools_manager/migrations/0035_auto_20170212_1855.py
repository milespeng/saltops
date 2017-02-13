# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 10:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tools_manager', '0034_auto_20170212_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolsexecdetailhistory',
            name='host',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.Host', verbose_name='目标主机'),
        ),
        migrations.AlterField(
            model_name='toolsexecdetailhistory',
            name='tool_exec_history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tools_manager.ToolsExecJob'),
        ),
        migrations.AlterField(
            model_name='toolsexecjob',
            name='tools',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools_manager.ToolsScript', verbose_name='工具'),
        ),
        migrations.AlterField(
            model_name='toolsscript',
            name='tools_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools_manager.ToolsTypes', verbose_name='工具类型'),
        ),
    ]
