# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-31 13:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sciunitmodels', '0009_modelinstance_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelinstance',
            name='timestamp',
            field=models.DateField(default=datetime.date.today),
        ),
    ]