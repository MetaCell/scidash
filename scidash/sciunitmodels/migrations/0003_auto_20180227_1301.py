# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-27 13:01
from __future__ import unicode_literals

import django.contrib.postgres.fields.hstore
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sciunitmodels', '0002_auto_20171226_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelinstance',
            name='run_params',
            field=django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True),
        ),
    ]
