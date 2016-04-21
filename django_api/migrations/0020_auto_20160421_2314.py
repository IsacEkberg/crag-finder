# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 21:14
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_api', '0019_auto_20160420_2323'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrustedAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='användare')),
            ],
            options={
                'verbose_name': 'klubbadministratör',
                'verbose_name_plural': 'klubbadministratörer',
            },
        ),
        migrations.RemoveField(
            model_name='clubadmin',
            name='club',
        ),
        migrations.RemoveField(
            model_name='clubadmin',
            name='user',
        ),
        migrations.AddField(
            model_name='areaimage',
            name='status',
            field=models.CharField(choices=[('b', 'väntar på godkännande'), ('a', 'Godkänt')], default='a', max_length=1),
        ),
        migrations.AddField(
            model_name='club',
            name='replacing',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_api.Club'),
        ),
        migrations.AddField(
            model_name='club',
            name='status',
            field=models.CharField(choices=[('b', 'väntar på godkännande'), ('a', 'Godkänt')], default='a', max_length=1),
        ),
        migrations.AddField(
            model_name='rockfaceimage',
            name='status',
            field=models.CharField(choices=[('b', 'väntar på godkännande'), ('a', 'Godkänt')], default='a', max_length=1),
        ),
        migrations.AlterField(
            model_name='rockface',
            name='geo_data',
            field=models.CharField(max_length=3000, null=True, validators=[django.core.validators.RegexValidator(code='invalid', message='Geo-data is malformed.', regex='^(\\(\\d{1,3}\\.\\d+, \\d{1,3}\\.\\d+\\);)*$')], verbose_name='plats för klippan'),
        ),
        migrations.DeleteModel(
            name='ClubAdmin',
        ),
    ]
