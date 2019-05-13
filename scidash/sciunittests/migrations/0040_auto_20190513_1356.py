# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-05-13 13:56
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sciunittests', '0039_auto_20190513_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testclass',
            name='observation_schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}),
        ),
        migrations.AlterField(
            model_name='testclass',
            name='test_parameters_schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}),
        ),
    ]
