# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-04 02:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_auto_20170904_0055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='image',
        ),
    ]
