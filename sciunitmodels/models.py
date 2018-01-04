from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import HStoreField


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
    url = models.URLField(default='', null=True, blank=True)

    class Meta:
        verbose_name = 'Model class'
        verbose_name_plural = 'Model classes'

    def __str__(self):
        return self.class_name


class ModelInstance(models.Model):
    model_class = models.ForeignKey(ModelClass)
    attributes = HStoreField()
    name = models.CharField(max_length=50)
    run_params = HStoreField()
    url = models.URLField(default='', null=True, blank=True)

    class Meta:
        verbose_name = 'Model instance'
        verbose_name_plural = 'Model instance'

    def __str__(self):
        return self.name
