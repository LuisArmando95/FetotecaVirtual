# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-04 20:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embriologia', '0013_auto_20170904_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='feto',
            name='tipo',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
