from rest_framework import viewsets, permissions

from sciunittests.serializers import ScoreSerializer, TestInstanceSerializer, \
                                    TestSuiteSerializer, TestClassSerializer

from sciunittests.models import Score, TestInstance, TestSuite, TestClass
from sciunittests.filters import ScoreFilter, TestSuiteFilter


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = (permissions.AllowAny,)
    filter_class = ScoreFilter


class TestInstanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TestInstance.objects.all()
    serializer_class = TestInstanceSerializer
    permission_classes = (permissions.AllowAny,)


class TestSuiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializer
    permission_classes = (permissions.AllowAny,)
    filter_class = TestSuiteFilter


class TestClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TestClass.objects.all()
    serializer_class = TestClassSerializer
    permission_classes = (permissions.AllowAny,)
    filter_fields = ('class_name',)
