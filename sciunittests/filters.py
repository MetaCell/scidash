from django_filters import rest_framework as filters
from sciunittests.models import Score, TestSuite, TestInstance


class ScoreFilter(filters.FilterSet):
    timestamp_after = filters.IsoDateTimeFilter(name='timestamp',
            lookup_expr='gte')
    timestamp_before = filters.IsoDateTimeFilter(name='timestamp',
            lookup_expr='lte')

    class Meta:
        model = Score
        fields = ['owner',
                'model_instance',
                'model_instance__model_class__class_name',
                'test_instance__test_class__class_name',
                'test_instance__hostname',
                'test_instance__build_info',
                'score_type',
                'timestamp_after',
                'timestamp_before']


class TestSuiteFilter(filters.FilterSet):
    timestamp_after = filters.IsoDateTimeFilter(name='timestamp',
            lookup_expr='gte')
    timestamp_before = filters.IsoDateTimeFilter(name='timestamp',
            lookup_expr='lte')

    class Meta:
        model = TestSuite
        fields = ['owner', 'timestamp_after', 'timestamp_before']


class TestInstanceFilter(filters.FilterSet):

    class Meta:
        model = TestInstance
        fields = ['hostname']
