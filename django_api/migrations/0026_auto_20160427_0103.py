# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0025_auto_20160423_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='name',
            field=models.CharField(max_length=150, verbose_name='namn'),
        ),
    ]
