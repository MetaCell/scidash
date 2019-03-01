from __future__ import unicode_literals

from datetime import date

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import HStoreField, JSONField
from django.db import models

from scidash.general import models as general_models
from scidash.sciunitmodels.helpers import (
    get_extra_capabilities, get_model_capabilities
)

# Models Related


class Capability(models.Model):
    class_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Capabilities'

    def __str__(self):
        return self.class_name


class CapabilityModelThrough(models.Model):
    capability = models.ForeignKey(Capability, on_delete=models.CASCADE)
    model_class = models.ForeignKey('ModelClass', on_delete=models.CASCADE)
    extra_check = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.capability.class_name} with check in {self.extra_check}'

    class Meta:
        verbose_name = 'Capabilities with extra check'
        verbose_name_plural = 'Capabilities with extra checks'


class ModelClass(models.Model):
    class_name = models.CharField(max_length=50)
    capabilities = models.ManyToManyField(
        Capability, blank=True, related_name='capabilities'
    )
    extra_capabilities = models.ManyToManyField(
        Capability,
        through=CapabilityModelThrough,
        related_name='capabilities_with_check',
        blank=True
    )
    url = models.URLField(default='', null=True, blank=True, unique=True)
    import_path = models.TextField(null=True, blank=True)
    memo = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        capabilities = []
        extra_capabilities = []

        try:
            capabilities = get_model_capabilities(self.import_path)
            extra_capabilities = get_extra_capabilities(self.import_path)
        except ImportError:
            self.memo = f"Can't import {self.import_path}"
        except AttributeError:
            self.memo = \
                f"Wrong class for import {self.import_path}"

        if capabilities is None:
            self.memo = \
                f"Wrong class for import capabilities {self.import_path}"
        elif extra_capabilities is None:
            self.memo = \
                f"No extra capabilities check {self.import_path}"

        for capability in capabilities:
            capability_model, created = Capability.objects.get_or_create(
                class_name=capability.__name__
            )
            if capability not in extra_capabilities:
                self.capabilities.add(capability_model)
            else:
                extra_capability_model, created = CapabilityModelThrough.objects.get_or_create(
                        capability=capability_model,
                        model_class=self,
                        extra_check=extra_capabilities[capability]
                )
                extra_capability_model.save()

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
