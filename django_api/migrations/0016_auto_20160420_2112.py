# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0015_auto_20160414_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='nr_of_bolts',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='antal bultar'),
        ),
        migrations.AlterField(
            model_name='route',
            name='grade',
            field=models.CharField(choices=[('no', 'Ej graderad'), ('4a-', '4a-'), ('4a', '4a'), ('4a+', '4a+'), ('4b-', '4b-'), ('4b', '4b'), ('4b+', '4b+'), ('4c-', '4c-'), ('4c', '4c'), ('4c+', '4c+'), ('5a-', '5a-'), ('5a', '5a'), ('5a+', '5a+'), ('5b-', '5b-'), ('5b', '5b'), ('5b+', '5b+'), ('5c-', '5c-'), ('5c', '5c'), ('5c+', '5c+'), ('6a-', '6a-'), ('6a', '6a'), ('6a+', '6a+'), ('6b-', '6b-'), ('6b', '6b'), ('6b+', '6b+'), ('6c-', '6c-'), ('6c', '6c'), ('6c+', '6c+'), ('7a-', '7a-'), ('7a', '7a'), ('7a+', '7a+'), ('7b-', '7b-'), ('7b', '7b'), ('7b+', '7b+'), ('7c-', '7c-'), ('7c', '7c'), ('7c+', '7c+'), ('8a-', '8a-'), ('8a', '8a'), ('8a+', '8a+'), ('8b-', '8b-'), ('8b', '8b'), ('8b+', '8b+'), ('8c-', '8c-'), ('8c', '8c'), ('8c+', '8c+'), ('9a-', '9a-'), ('9a', '9a'), ('9a+', '9a+'), ('9b-', '9b-'), ('9b', '9b'), ('9b+', '9b+'), ('9c-', '9c-'), ('9c', '9c'), ('9c+', '9c+')], default='no', max_length=3, verbose_name='gradering'),
        ),
    ]