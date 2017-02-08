# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 02:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy_manager', '0025_projectversion_subplaybook'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectversion',
            name='sub_job_script_type',
            field=models.IntegerField(choices=[(0, 'sls'), (1, 'shell')], default=0, verbose_name='脚本语言'),
        ),
    ]
