# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-04 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0005_auto_20160404_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='length',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
