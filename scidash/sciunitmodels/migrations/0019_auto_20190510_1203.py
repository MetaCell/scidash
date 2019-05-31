# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-05-10 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sciunitmodels', '0018_auto_20190510_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelclass',
            name='extra_capabilities',
            field=models.ManyToManyField(blank=True, related_name='extra_capabilities', through='sciunitmodels.ExtraCapabilityModelThrough', to='sciunitmodels.Capability'),
        ),
    ]