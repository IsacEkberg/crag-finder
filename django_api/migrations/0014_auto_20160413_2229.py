# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-13 20:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0013_auto_20160412_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='rockfaceimage',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='kort beskrivning av bilden'),
        ),
        migrations.AddField(
            model_name='rockfaceimage',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='namn'),
        ),
        migrations.AddField(
            model_name='route',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_api.RockFaceImage'),
        ),
        migrations.AddField(
            model_name='route',
            name='route_nr',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Lednummer'),
        ),
    ]