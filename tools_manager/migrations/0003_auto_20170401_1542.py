# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools_manager', '0002_auto_20170303_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolsscript',
            name='tool_run_type',
            field=models.IntegerField(choices=[(0, 'SaltState'), (1, 'Shell'), (2, 'PowerShell'), (3, 'Python'), (4, 'Salt命令'), (5, 'Windows批处理')], default=0, verbose_name='脚本类型'),
        ),
    ]