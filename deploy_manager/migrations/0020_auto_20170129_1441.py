# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 06:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy_manager', '0019_auto_20170129_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='playbook',
            field=models.TextField(blank=True, help_text='${version}代表默认版本号', null=True, verbose_name='部署脚本'),
        ),
    ]
