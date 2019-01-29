from django.db.models import Count, Q, Subquery
from django_filters import rest_framework as filters

from scidash.sciunittests.models import ScoreInstance, TestInstance, TestSuite


class TestInstanceFilter(filters.FilterSet):
    class_name = filters.CharFilter(
        name='test_class__class_name',
        lookup_expr='icontains'
    )

    tags = filters.CharFilter(
        name='tags__name',
        lookup_expr='icontains'
    )

    name = filters.CharFilter(name='test_class__class_name',
                              lookup_expr='icontains')

    timestamp_from = filters.IsoDateTimeFilter(name='timestamp',
            lookup_expr='gte')

    timestamp_to = filters.IsoDateTimeFilter(name='timestamp',
            lookup_expr='lte')

    class Meta:
        model = TestInstance
        fields = [
            'name',
            'class_name',
            'tags',
            'timestamp_from',
            'timestamp_to'
        ]


class ScoreFilter(filters.FilterSet):
    owner = filters.CharFilter(name='owner__username', lookup_expr='icontains')

    timestamp_from = filters.IsoDateTimeFilter(
        name='timestamp', lookup_expr='gte'
    )

    timestamp_to = filters.IsoDateTimeFilter(
        name='timestamp', lookup_expr='lte'
    )

    model = filters.CharFilter(method='model_class_name_filter')

    test_class = filters.CharFilter(
        name='test_instance__test_class__class_name', lookup_expr='icontains'
    )

    hostname = filters.CharFilter(
        name='test_instance__hostname', lookup_expr='icontains'
    )

    name = filters.CharFilter(
        name='test_instance__test_class__class_name', lookup_expr='icontains'
    )

    score_type = filters.CharFilter(name='score_type', lookup_expr='icontains')

    build_info = filters.CharFilter(
        name='test_instance__build_info', lookup_expr='icontains'
    )

    with_suites = filters.BooleanFilter(method='with_suites_filter')

    suite_name = filters.CharFilter(method='suite_name_filter')

    suite_hash = filters.CharFilter(method='suite_hash_filter')

    def model_class_name_filter(self, queryset, name, value):
        return ScoreInstance.objects.filter(
            Q(model_instance__model_class__class_name__icontains=value)
            | Q(model_instance__name__icontains=value)
        )

    def with_suites_filter(self, queryset, name, value):
        tests = TestInstance.objects.prefetch_related('test_suites')
        tests = tests.annotate(Count('test_suites'))
        tests = tests.filter(test_suites__count__gt=0)

        return queryset.filter(test_instance__in=tests)

    def suite_name_filter(self, queryset, name, value):
        suites = TestSuite.objects.filter(name__icontains=value)

        kwargs = {
            'test_instance__test_suites__in': Subquery(suites.values('pk'))
        }

        return queryset.filter(**kwargs)

    def suite_hash_filter(self, queryset, name, value):

        suites = TestSuite.objects.filter(hash=value)

        kwargs = {
            'test_instance__test_suites__in': Subquery(suites.values('pk'))
        }

        return queryset.filter(**kwargs)

    class Meta:
        model = ScoreInstance
        fields = [
            'owner', 'model_instance', 'model', 'test_class', 'name',
            'hostname', 'build_info', 'with_suites', 'suite_name',
            'suite_hash', 'score_type', 'timestamp_from', 'timestamp_to'
        ]


class TestSuiteFilter(filters.FilterSet):
    timestamp_after = filters.IsoDateTimeFilter(
        name='timestamp', lookup_expr='gte'
    )
    timestamp_before = filters.IsoDateTimeFilter(
        name='timestamp', lookup_expr='lte'
    )

    class Meta:
        model = TestSuite
        fields = ['owner', 'timestamp_after', 'timestamp_before']