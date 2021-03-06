# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-08 11:40
from __future__ import unicode_literals

import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Capability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Capabilities',
            },
        ),
        migrations.CreateModel(
            name='ModelClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=50)),
                ('capabilities', models.ManyToManyField(to='sciunitmodels.Capability')),
            ],
            options={
                'verbose_name': 'Model class',
                'verbose_name_plural': 'Model classes',
            },
        ),
        migrations.CreateModel(
            name='ModelInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributes', django.contrib.postgres.fields.hstore.HStoreField()),
                ('name', models.CharField(max_length=50)),
                ('run_params', django.contrib.postgres.fields.hstore.HStoreField()),
                ('url', models.URLField()),
                ('model_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sciunitmodels.ModelClass')),
            ],
            options={
                'verbose_name': 'Model instance',
                'verbose_name_plural': 'Model instance',
            },
        ),
    ]
