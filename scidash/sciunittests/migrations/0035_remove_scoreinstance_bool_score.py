# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-04-15 14:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sciunittests', '0034_auto_20190415_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scoreinstance',
            name='bool_score',
        ),
    ]
