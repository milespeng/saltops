# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 08:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy_manager', '0040_projectconfigpath_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectconfigpath',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projecthost',
            name='config',
        ),
        migrations.DeleteModel(
            name='ProjectConfig',
        ),
        migrations.DeleteModel(
            name='ProjectConfigPath',
        ),
    ]
