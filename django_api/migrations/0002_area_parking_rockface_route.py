# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-28 18:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parking', to='django_api.Area')),
            ],
        ),
        migrations.CreateModel(
            name='RockFace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rockfaces', to='django_api.Area')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('grade', models.CharField(choices=[('no', 'Ej graderad'), ('4a', '4a'), ('4b', '4b'), ('4c', '4c'), ('5a', '5a'), ('5b', '5b'), ('5c', '5c'), ('6a-', '6a-'), ('6a', '6a'), ('6a+', '6a+'), ('6b-', '6b-'), ('6b', '6b'), ('6b+', '6b+'), ('6c-', '6c-'), ('6c', '6c'), ('6c+', '6c+'), ('7a-', '7a-'), ('7a', '7a'), ('7a+', '7a+'), ('7b-', '7b-'), ('7b', '7b'), ('7b+', '7b+'), ('7c-', '7c-'), ('7c', '7c'), ('7c+', '7c+'), ('8a-', '8a-'), ('8a', '8a'), ('8a+', '8a+'), ('8b-', '8b-'), ('8b', '8b'), ('8b+', '8b+'), ('8c-', '8c-'), ('8c', '8c'), ('8c+', '8c+'), ('9a-', '9a-'), ('9a', '9a'), ('9a+', '9a+'), ('9b-', '9b-'), ('9b', '9b'), ('9b+', '9b+'), ('9c-', '9c-'), ('9c', '9c'), ('9c+', '9c+')], default='no', max_length=3)),
                ('type', models.CharField(choices=[('Bo', 'Boulder'), ('Sp', 'Sport'), ('Tr', 'Trad'), ('Ai', 'Aid'), ('DW', 'DWS')], default='Sp', max_length=2)),
                ('rock_face', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='django_api.RockFace')),
            ],
        ),
    ]
