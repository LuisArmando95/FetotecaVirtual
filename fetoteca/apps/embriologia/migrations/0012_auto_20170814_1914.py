# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-14 19:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('embriologia', '0011_auto_20170814_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feto',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
