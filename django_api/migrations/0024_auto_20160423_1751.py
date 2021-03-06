# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-23 15:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0023_auto_20160423_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='typ'),
        ),
        migrations.AlterField(
            model_name='change',
            name='creation_date',
            field=models.DateTimeField(auto_created=True, verbose_name='datum'),
        ),
        migrations.AlterField(
            model_name='change',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='användare'),
        ),
    ]
