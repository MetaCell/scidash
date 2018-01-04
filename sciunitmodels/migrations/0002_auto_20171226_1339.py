# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-26 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sciunitmodels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelclass',
            name='url',
            field=models.URLField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='modelinstance',
            name='url',
            field=models.URLField(blank=True, default='', null=True),
        ),
    ]
