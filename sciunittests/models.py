from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.utils import timezone

import sciunitmodels
from general import models as general_models


class TestSuite(models.Model):
    name = models.CharField(max_length=50)
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
    test_suites = models.ManyToManyField(TestSuite)
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


class Score(models.Model):
    score_type = models.CharField(max_length=200, default='', null=True,
            blank=True)
    model_instance = models.ForeignKey(sciunitmodels.models.ModelInstance)
    test_instance = models.ForeignKey(TestInstance)
    score = models.FloatField(default=0)
    sort_key = models.FloatField(default=0)
    prediction = models.FloatField(default=0)
    related_data = HStoreField()
    timestamp = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(general_models.ScidashUser, default=None)

    def __str__(self):
        return "Score for {0} in {1} test instance".format(
            self.model_instance.name,
            self.test_instance.test_class.class_name
        )
