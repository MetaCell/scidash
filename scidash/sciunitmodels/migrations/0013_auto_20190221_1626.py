# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-21 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sciunitmodels', '0012_modelclass_import_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='CapabilityModelThrough',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_check', models.CharField(max_length=300)),
                ('capability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sciunitmodels.Capability')),
                ('model_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sciunitmodels.ModelClass')),
            ],
        ),
        migrations.AddField(
            model_name='modelclass',
            name='extra_capabilities',
            field=models.ManyToManyField(related_name='extra_capabilities_set', through='sciunitmodels.CapabilityModelThrough', to='sciunitmodels.Capability'),
        ),
    ]