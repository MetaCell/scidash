# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-03 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logviewer', '0003_auto_20200303_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logfile',
            name='path',
            field=models.FilePathField(allow_folders=True, match='.*\\.log$', path='/opt/projects/metacell/scidash/scidash', recursive=True),
        ),
    ]