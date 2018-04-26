import logging

from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.utils import timezone

import sciunitmodels
from general import models as general_models

logger = logging.getLogger(__name__)


class TestSuite(models.Model):
    name = models.CharField(max_length=50)
    hash = models.CharField(max_length=57, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(general_models.ScidashUser, default=None)

    class Meta:
        verbose_name = 'Test suite'
        verbose_name_plural = 'Test suites'

    def __str__(self):
        return self.name


class TestClass(models.Model):
    class_name = models.CharField(max_length=50)
    url = models.URLField(default='', null=True, blank=True)

    class Meta:
        verbose_name = 'Test class'
        verbose_name_plural = 'Test classes'

    def __str__(self):
        return self.class_name


class TestInstance(models.Model):
    test_class = models.ForeignKey(TestClass)
    observation = HStoreField()
    test_suites = models.ManyToManyField(TestSuite, related_name='tests')
    description = models.TextField(blank=True, null=True)
    verbose = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    hostname = models.CharField(max_length=200, default='', blank=True,
            null=True)
    build_info = models.CharField(max_length=200, default='', blank=True,
            null=True)

    class Meta:
        verbose_name = 'Test instance'
        verbose_name_plural = 'Test instances'

    def __str__(self):
        return "{0} instance".format(self.test_class.class_name)


class ScoreClass(models.Model):
    class_name = models.CharField(max_length=200)
    url = models.URLField(default='', null=True, blank=True)

    class Meta:
        verbose_name = "Score Class"
        verbose_name_plural = "Score Classes"

    def __str__(self):
        return self.class_name


class ScoreInstance(models.Model):
    score_type = models.CharField(max_length=200, default='', null=True,
            blank=True)
    score_class = models.ForeignKey(ScoreClass)
    model_instance = models.ForeignKey(sciunitmodels.models.ModelInstance)
    test_instance = models.ForeignKey(TestInstance)
    score = models.FloatField(default=0)
    sort_key = models.FloatField(default=0)
    prediction_numeric = models.FloatField(default=None, null=True, blank=True)
    prediction_dict = HStoreField(default=None, null=True, blank=True)
    raw = models.CharField(max_length=200, default=None, blank=True, null=True)
    summary = models.CharField(max_length=200,
                               default=None, blank=True, null=True)
    related_data = HStoreField()
    timestamp = models.DateTimeField(default=timezone.now)
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
            self.model_instance.name,
            self.test_instance.test_class.class_name
        )
