# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-14 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0029_auto_20160614_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access',
            name='rock_face',
            field=models.ManyToManyField(related_name='access', to='django_api.RockFace', verbose_name='klippa'),
        ),
    ]