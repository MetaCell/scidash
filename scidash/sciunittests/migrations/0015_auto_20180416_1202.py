# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-16 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sciunittests', '0014_merge_20180404_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScoreClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=200)),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'Score Class',
                'verbose_name_plural': 'Score Classes',
            },
        ),
        migrations.RenameModel(
            old_name='Score',
            new_name='ScoreInstance',
        ),
    ]
