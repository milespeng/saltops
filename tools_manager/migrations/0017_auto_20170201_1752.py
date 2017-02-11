# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 09:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tools_manager', '0016_auto_20170201_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolsparam',
            name='tool_script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools_manager.ToolsScript', verbose_name='工具'),
        ),
        migrations.AlterField(
            model_name='toolsscript',
            name='tools_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools_manager.ToolsTypes', verbose_name='工具类型'),
        ),
    ]
