# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-30 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0003_parking_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='rockface',
            name='geo_data',
            field=models.CharField(max_length=3000, null=True),
        ),
    ]
