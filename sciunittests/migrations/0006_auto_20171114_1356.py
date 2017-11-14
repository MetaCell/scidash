# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-14 13:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sciunittests', '0005_testinstance_verbose'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 14, 13, 56, 50, 366805)),
        ),
        migrations.AddField(
            model_name='testclass',
            name='build_info',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='testclass',
            name='hostname',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='testclass',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 14, 13, 56, 50, 365364)),
        ),
        migrations.AddField(
            model_name='testsuite',
            name='build_info',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='testsuite',
            name='hostname',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='testsuite',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 14, 13, 56, 50, 364644)),
        ),
    ]
