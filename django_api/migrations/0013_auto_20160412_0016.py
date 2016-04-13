# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-11 22:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0012_auto_20160411_2334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rockfaceimage',
            name='area',
        ),
        migrations.AddField(
            model_name='rockfaceimage',
            name='rockface',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='image', to='django_api.RockFace'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='areaimage',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='django_api.Area'),
        ),
    ]
