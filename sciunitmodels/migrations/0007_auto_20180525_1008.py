# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-25 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sciunitmodels', '0006_modelinstance_hash_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelclass',
            name='url',
            field=models.URLField(blank=True, default='', null=True, unique=True),
        ),
    ]