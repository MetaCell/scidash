# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-05-20 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FilePathField(match='*\\.log', recursive=True, verbose_name='/Users/roman/Projects/metacell/scidash')),
                ('name', models.CharField(default='Log file', max_length=200)),
            ],
        ),
    ]