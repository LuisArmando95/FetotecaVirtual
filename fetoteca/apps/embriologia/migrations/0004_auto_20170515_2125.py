# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 21:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embriologia', '0003_auto_20170515_1815'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feto',
            old_name='gestacion',
            new_name='semanagestacion',
        ),
    ]