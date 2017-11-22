from django_filters import rest_framework as filters
from sciunittests.models import Score, TestSuite


class ScoreFilter(filters.FilterSet):
    timestamp = filters.DateFromToRangeFilter()

    class Meta:
        model = Score
        fields = ['owner', 'model_instance__model_class__class_name',
                'model_instance', 'timestamp']


class TestSuiteFilter(filters.FilterSet):
    timestamp = filters.DateFromToRangeFilter()

    class Meta:
        model = TestSuite
        fields = ['owner', 'timestamp']
