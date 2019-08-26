from __future__ import unicode_literals

import logging
from datetime import datetime as date

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from scidash.general import models as general_models
from scidash.sciunitmodels.helpers import (
    get_extra_capabilities, get_model_capabilities
)

db_logger = logging.getLogger('db')


class Capability(models.Model):
    class_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Capabilities'

    def __str__(self):
        return self.class_name


class ExtraCapabilityModelThrough(models.Model):
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
        Capability, blank=True, related_name='model_classes'
    )
    extra_capabilities = models.ManyToManyField(
        Capability, through=ExtraCapabilityModelThrough, blank=True
    )
    url = models.URLField(default='', null=True, blank=True, unique=True)
    import_path = models.TextField(default='', null=True, blank=True)
    memo = models.TextField(null=True, blank=True)

    def populate_capabilities(self):
        if self.import_path == '':
            return

        capabilities = []
        extra_capabilities = []

        try:
            capabilities = get_model_capabilities(self.import_path)
            extra_capabilities = get_extra_capabilities(self.import_path)
        except ImportError:
            db_logger.exception(f"Can't import {self.import_path}")
        except AttributeError:
            db_logger.exception(f"Wrong class for import {self.import_path}")

        if capabilities is None:
            db_logger.exception(
                f"Wrong class for import capabilities {self.import_path}"
            )
        elif extra_capabilities is None:
            db_logger.exception(
                f"No extra capabilities check {self.import_path}"
            )

        for capability in capabilities:
            capability_model, created = Capability.objects.get_or_create(
                class_name=capability.__name__
            )
            if extra_capabilities is None or capability not in extra_capabilities.keys(
            ):  # noqa: E501
                self.capabilities.add(capability_model)
            else:
                extra_capability_model, created = ExtraCapabilityModelThrough.objects.get_or_create(  # noqa: E501
                    capability=capability_model,
                    model_class=self,
                    extra_check=extra_capabilities[capability]
                )
                extra_capability_model.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.populate_capabilities()

    class Meta:
        verbose_name = 'Model class'
        verbose_name_plural = 'Model classes'

    def __str__(self):
        return self.class_name


class ModelInstance(models.Model):
    LOCKED = 'l'
    AVAILABLE = 'a'

    STATUS_CHOICES = (
        (LOCKED, 'Locked'),
        (AVAILABLE, 'Available'),
    )

    model_class = models.ForeignKey(ModelClass)
    backend = models.CharField(max_length=200, null=True, blank=True)
    attributes = JSONField(blank=True, null=True)
    name = models.CharField(max_length=50)
    run_params = JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=AVAILABLE
    )
    owner = models.ForeignKey(general_models.ScidashUser, null=True)
    hash_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)
    url = models.URLField(default='', null=True, blank=True)
    tags = GenericRelation(general_models.Tag)

    class Meta:
        verbose_name = 'Model instance'
        verbose_name_plural = 'Model instance'

    def __str__(self):
        return self.name
