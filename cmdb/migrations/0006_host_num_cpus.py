# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 14:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0005_hostip_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='num_cpus',
            field=models.IntegerField(blank=True, null=True, verbose_name='CPU\u6570\u91cf'),
        ),
    ]
