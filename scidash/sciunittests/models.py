import json
import logging
from datetime import datetime as date

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import HStoreField, JSONField
from django.db import models

import scidash.sciunitmodels as sciunitmodels
from scidash.general import models as general_models
from scidash.general.helpers import import_class
from scidash.sciunittests.constants import TEST_PARAMS_UNITS_TYPE
from scidash.sciunittests.helpers import (
    build_destructured_unit, get_observation_schema, get_test_parameters_schema,
    get_units, get_default_params
)

import quantities
import numbers

db_logger = logging.getLogger('db')

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        quantities.set_default_units(time='s', current='A')
        if isinstance(obj, quantities.quantity.Quantity):
            return float(obj.simplified.magnitude)
        elif isinstance(obj, numbers.Number):
            # Noticed Sciunit does not use always quantities, 
            # this will avoid the entire UI to explode
            return float(obj)
        else:
            db_logger.exception(f"I do not know this unit: {obj}")


class TestSuite(models.Model):
    name = models.CharField(max_length=50)
    hash = models.CharField(max_length=57, null=True, blank=True)
    timestamp = models.DateTimeField(default=date.today)
    owner = models.ForeignKey(general_models.ScidashUser, default=None)

    class Meta:
        verbose_name = 'Test suite'
        verbose_name_plural = 'Test suites'

    def __str__(self):
        return self.name


class TestClass(models.Model):
    class_name = models.CharField(max_length=50)
    url = models.URLField(default='', null=True, blank=True)
    import_path = models.TextField(null=True, blank=True)
    observation_schema = JSONField(null=True, blank=True)
    test_parameters_schema = JSONField(null=True, blank=True)
    units = models.TextField(null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    params_units = JSONField(null=True, blank=True)
    default_params = JSONField(encoder=JSONEncoder , null=True, blank=True)

    class Meta:
        verbose_name = 'Test class'
        verbose_name_plural = 'Test classes'

    def units_name(self):
        try:
            destructured = json.loads(self.units)
        except (json.JSONDecodeError, TypeError):
            if self.units is not None:
                return import_class(self.units).name
            else:
                return "N/A"

        if destructured.get('name', False):
            return build_destructured_unit(destructured).name
        else:
            return ' | '.join(
                [
                    import_class(value).name
                    for key, value in destructured.items()
                ]
            )

    def __str__(self):
        return self.class_name

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        if self.import_path == '':
            return

        observation_schema = None
        params_schema = None
        units = None
        params_units = {}
        default_params = None

        try:
            observation_schema = get_observation_schema(self.import_path)
            params_schema = get_test_parameters_schema(self.import_path)
            units = get_units(self.import_path)
            default_params = get_default_params(self.import_path)
        except ImportError:
            db_logger.exception(f"Can't import {self.import_path}")
        except AttributeError:
            db_logger.exception(f"Can't import {self.import_path}")

        if observation_schema is None:
            db_logger.exception(
                f"Observation schema not found {self.import_path}"
            )

        if params_schema is None:
            db_logger.exception(f"Params schema not found {self.import_path}")

        if units is None:
            db_logger.exception(f"Units not found {self.import_path}")

        if default_params is None:
            db_logger.exception(f"Default params not found {self.import_path}")

        self.observation_schema = observation_schema
        self.test_parameters_schema = params_schema
        self.default_params = default_params

        if params_schema is not None:
            for key in params_schema:
                params_units[key] = TEST_PARAMS_UNITS_TYPE[params_schema[key]
                                                           ['type']]

        self.units = units
        self.params_units = params_units


class TestInstance(models.Model):
    LOCKED = 'l'
    AVAILABLE = 'a'

    STATUS_CHOICES = (
        (LOCKED, 'Locked'),
        (AVAILABLE, 'Available'),
    )

    name = models.CharField(max_length=200, default='Default Name')
    test_class = models.ForeignKey(TestClass)
    observation = JSONField(null=True, blank=True)
    params = JSONField(null=True, blank=True)
    test_suites = models.ManyToManyField(
        TestSuite, related_name='tests', blank=True
    )
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(general_models.ScidashUser, null=True)
    verbose = models.IntegerField(default=0)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=AVAILABLE
    )
    timestamp = models.DateTimeField(auto_now=True)
    hash_id = models.CharField(max_length=100)
    hostname = models.CharField(
        max_length=200, default='', blank=True, null=True
    )
    build_info = models.CharField(
        max_length=200, default='', blank=True, null=True
    )
    tags = GenericRelation(general_models.Tag)

    class Meta:
        verbose_name = 'Test instance'
        verbose_name_plural = 'Test instances'

    def __str__(self):
        return f"{self.name} - {self.test_class.class_name} instance"


class ScoreClass(models.Model):
    class_name = models.CharField(max_length=200)
    url = models.URLField(default='', null=True, blank=True)

    class Meta:
        verbose_name = "Score Class"
        verbose_name_plural = "Score Classes"

    def __str__(self):
        return self.class_name


class ScoreInstance(models.Model):
    SCHEDULED = 's'
    LOCKED = 'l'
    CALCULATED = 'c'
    FAILED = 'f'

    STATUS_CHOICES = (
        (SCHEDULED, 'Scheduled'), (CALCULATED, 'Calculated'),
        (LOCKED, 'Locked'), (FAILED, 'Failed')
    )

    score_type = models.CharField(
        max_length=200, default='', null=True, blank=True
    )
    score_class = models.ForeignKey(ScoreClass, null=True, blank=True)
    model_instance = models.ForeignKey(
        sciunitmodels.models.ModelInstance, related_name='score'
    )
    test_instance = models.ForeignKey(TestInstance, related_name='score')
    score = models.FloatField(default=0, null=True, blank=True)
    sort_key = models.FloatField(default=0)
    prediction_numeric = models.FloatField(default=None, null=True, blank=True)
    prediction_dict = HStoreField(default=None, null=True, blank=True)
    raw = models.CharField(max_length=200, default=None, blank=True, null=True)
    hash_id = models.CharField(max_length=100)
    status = models.CharField(
        max_length=3, choices=STATUS_CHOICES, default='c'
    )
    summary = models.CharField(
        max_length=200, default=None, blank=True, null=True
    )
    timestamp = models.DateTimeField(default=date.today)
    owner = models.ForeignKey(general_models.ScidashUser, default=None)
    error = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.test_instance.status = TestInstance.LOCKED
        self.test_instance.save()

        self.model_instance.status = sciunitmodels.models.ModelInstance.LOCKED
        self.model_instance.save()

    @property
    def prediction(self):
        """
        Alias for prediction, automatically detects type of prediction and
        returns to corresponding field
        :returns: dict or float
        """
        if self.prediction_numeric is not None:
            return self.prediction_numeric

        return self.prediction_dict

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp',]),
        ]

    def __str__(self):
        return "Score for {0} in {1} test instance".format(
            self.model_instance.name, self.test_instance.test_class.class_name
        )
