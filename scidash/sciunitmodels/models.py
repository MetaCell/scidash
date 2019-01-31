from __future__ import unicode_literals
from datetime import date

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import HStoreField, JSONField
from django.db import models

from scidash.general import models as general_models

# Models Related


class Capability(models.Model):
    class_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Capabilities'

    def __str__(self):
        return self.class_name


class ModelClass(models.Model):
    class_name = models.CharField(max_length=50)
    capabilities = models.ManyToManyField(Capability)
    url = models.URLField(default='', null=True, blank=True, unique=True)

    class Meta:
        verbose_name = 'Model class'
        verbose_name_plural = 'Model classes'

    def __str__(self):
        return self.class_name


class ModelInstance(models.Model):
    model_class = models.ForeignKey(ModelClass)
    backend = models.CharField(max_length=200, null=True, blank=True)
    attributes = JSONField(blank=True, null=True)
    name = models.CharField(max_length=50)
    run_params = HStoreField(blank=True, null=True)
    owner = models.ForeignKey(general_models.ScidashUser, null=True)
    hash_id = models.CharField(max_length=100)
    timestamp = models.DateField(default=date.today)
    url = models.URLField(default='', null=True, blank=True)
    tags = GenericRelation(general_models.Tag)

    class Meta:
        verbose_name = 'Model instance'
        verbose_name_plural = 'Model instance'

    def __str__(self):
        return self.name
