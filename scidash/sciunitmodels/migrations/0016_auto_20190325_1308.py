# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-03-25 13:08
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sciunitmodels', '0015_modelclass_memo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelinstance',
            name='run_params',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
