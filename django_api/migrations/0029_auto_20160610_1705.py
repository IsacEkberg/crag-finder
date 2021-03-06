# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-10 15:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0028_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos_x', models.IntegerField()),
                ('pos_y', models.IntegerField()),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_api.RockFaceImage')),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='route_nodes',
            field=models.ManyToManyField(to='django_api.RouteNode'),
        ),
    ]
