# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-04 00:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20170516_0229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='apellidos',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='email',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='password',
        ),
        migrations.AddField(
            model_name='usuario',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='sexo',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
