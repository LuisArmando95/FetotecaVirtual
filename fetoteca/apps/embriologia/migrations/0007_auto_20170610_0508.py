# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-10 05:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embriologia', '0006_auto_20170518_0627'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SemanaGestacional',
            new_name='PeriodoPrenatal',
        ),
        migrations.RenameField(
            model_name='feto',
            old_name='semanagestacion',
            new_name='periodo',
        ),
    ]