import logging
from datetime import date

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import HStoreField, JSONField
from django.db import models

import scidash.sciunitmodels as sciunitmodels
from scidash.general import models as general_models
from scidash.general.helpers import import_class
from scidash.sciunittests.helpers import (
    get_observation_schema, get_test_parameters_schema, get_units
)

logger = logging.getLogger(__name__)


class TestSuite(models.Model):
    name = models.CharField(max_length=50)
    hash = models.CharField(max_length=57, null=True, blank=True)
    timestamp = models.DateField(default=date.today)
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

    class Meta:
        verbose_name = 'Test class'
        verbose_name_plural = 'Test classes'

    def units_name(self):
        return import_class(self.units).name

    def __str__(self):
        return self.class_name

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        observation_schema = None
        params_schema = None
        units = None

        try:
            observation_schema = get_observation_schema(self.import_path)
            params_schema = get_test_parameters_schema(self.import_path)
            units = get_units(self.import_path)
        except ImportError:
            self.memo = f"Can't import {self.import_path}"
        except AttributeError:
            self.memo = \
                f"Wrong class for import {self.import_path}"

        if observation_schema is None:
            self.memo = \
                f"Wrong class for import observations {self.import_path}"
        elif params_schema is None:
            self.memo = \
                f"Wrong class for import params {self.import_path}"
        elif units is None:
            self.memo = \
                f"Wrong class for import dimensions {self.import_path}"
        else:
            self.memo = ""

        self.observation_schema = observation_schema
        self.test_parameters_schema = params_schema
        self.units = units


class TestInstance(models.Model):
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
    timestamp = models.DateField(default=date.today)
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
    score_type = models.CharField(
        max_length=200, default='', null=True, blank=True
    )
    score_class = models.ForeignKey(ScoreClass)
    model_instance = models.ForeignKey(sciunitmodels.models.ModelInstance)
    test_instance = models.ForeignKey(TestInstance)
    score = models.FloatField(default=0)
    sort_key = models.FloatField(default=0)
    prediction_numeric = models.FloatField(default=None, null=True, blank=True)
    prediction_dict = HStoreField(default=None, null=True, blank=True)
    raw = models.CharField(max_length=200, default=None, blank=True, null=True)
    hash_id = models.CharField(max_length=100)
    summary = models.CharField(
        max_length=200, default=None, blank=True, null=True
    )
    timestamp = models.DateField(default=date.today)
    owner = models.ForeignKey(general_models.ScidashUser, default=None)

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

    def __str__(self):
        return "Score for {0} in {1} test instance".format(
            self.model_instance.name, self.test_instance.test_class.class_name
        )
