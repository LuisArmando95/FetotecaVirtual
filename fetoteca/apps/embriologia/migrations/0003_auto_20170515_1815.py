# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 18:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('embriologia', '0002_feto_imagenes'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemanaGestacional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='feto',
            name='gestacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='embriologia.SemanaGestacional'),
        ),
    ]
