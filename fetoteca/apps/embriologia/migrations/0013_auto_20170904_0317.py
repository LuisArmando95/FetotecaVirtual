# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-04 03:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embriologia', '0012_auto_20170814_1914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
