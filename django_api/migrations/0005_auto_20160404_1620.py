# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-04 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0004_rockface_geo_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rental',
        ),
        migrations.AddField(
            model_name='area',
            name='long_description',
            field=models.CharField(max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='area',
            name='road_description',
            field=models.CharField(max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='area',
            name='short_description',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='rockface',
            name='long_description',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='rockface',
            name='short_description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='route',
            name='first_ascent_name',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='route',
            name='first_ascent_year',
            field=models.PositiveIntegerField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='route',
            name='length',
            field=models.PositiveIntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='route',
            name='short_description',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
    ]