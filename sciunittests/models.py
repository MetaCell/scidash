from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField

import sciunitmodels
# Create your models here.

# Tests related


class TestSuite(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Test suite'
        verbose_name_plural = 'Test suites'

    def __str__(self):
        return self.name


class TestClass(models.Model):
    class_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Test class'
        verbose_name_plural = 'Test classes'

    def __str__(self):
        return self.class_name


class TestInstance(models.Model):
    test_class = models.ForeignKey(TestClass)
    observation = models.CharField(max_length=50)
    test_suite = models.ForeignKey(TestSuite)

    class Meta:
        verbose_name = 'Test instance'
        verbose_name_plural = 'Test instances'

    def __str__(self):
        return "{0} instance".format(self.test_class.class_name)


class Score(models.Model):
    model_instance = models.ForeignKey(sciunitmodels.models.ModelInstance)
    test_instance = models.ForeignKey(TestInstance)
    score = models.FloatField()
    related_data = HStoreField()
    unpicklable = ArrayField(models.CharField(max_length=50))

    def __str__(self):
        return "Score for {0} in {1} test instance".format(
            self.model_instance.name,
            self.test_instance.test_class.class_name
        )
