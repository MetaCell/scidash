from django.db.models import Count, Subquery

from django_filters import rest_framework as filters
from sciunittests.models import ScoreInstance, TestSuite, TestInstance


class ScoreFilter(filters.FilterSet):
    owner = filters.CharFilter(name='owner__username',
            lookup_expr='startswith')

    timestamp_after = filters.IsoDateTimeFilter(name='timestamp',
            lookup_expr='gte')

    timestamp_before = filters.IsoDateTimeFilter(name='timestamp',
            lookup_expr='lte')

    model_class = filters.CharFilter(
            name='model_instance__model_class__class_name',
            lookup_expr='startswith' )

    test_class = filters.CharFilter(
            name='test_instance__test_class__class_name',
            lookup_expr='startswith' )

    hostname = filters.CharFilter(
            name='test_instance__hostname',
            lookup_expr='startswith' )

    score_name = filters.CharFilter(
            name='test_instance__test_class__class_name',
            lookup_expr='startswith' )

    score_type = filters.CharFilter(
            name='score_type',
            lookup_expr='startswith' )

    build_info = filters.CharFilter(
            name='test_instance__build_info',
            lookup_expr='startswith' )

    with_suites = filters.BooleanFilter(method='with_suites_filter')

    by_suite_name = filters.CharFilter(method='by_suite_name_filter')

    def with_suites_filter(self, queryset, name, value):
        tests = TestInstance.objects.prefetch_related('test_suites')
        tests = tests.annotate(Count('test_suites'))
        tests = tests.filter(test_suites__count__gt=0)

        return queryset.filter(test_instance__in=tests)

    def by_suite_name_filter(self, queryset, name, value):
        suites = TestSuite.objects.filter(name__startswith=value)

        kwargs = {
                'test_instance__test_suites__in':Subquery(suites.values('pk'))
                }

        return queryset.filter(**kwargs)

    class Meta:
        model = ScoreInstance
        fields = ['owner',
                'model_instance',
                'model_class',
                'test_class',
                'score_name',
                'hostname',
                'build_info',
                'with_suites',
                'by_suite_name',
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
