# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-11 17:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_api.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_api', '0009_auto_20160407_0010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=django_api.models._image_file_path, verbose_name='bild')),
                ('modified_by', models.ForeignKey(help_text='Uppladdat av.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='användare')),
            ],
        ),
    ]
