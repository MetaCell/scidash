from rest_framework import viewsets, permissions

from scidash.sciunittests.serializers import ScoreInstanceSerializer, \
                                    TestInstanceSerializer, \
                                    TestSuiteSerializer, TestClassSerializer, \
                                    ScoreClassSerializer

from scidash.sciunittests.models import ScoreInstance, \
                                    TestInstance, TestSuite, TestClass, \
                                    ScoreClass
from scidash.sciunittests.filters import ScoreFilter, TestSuiteFilter, \
                                TestInstanceFilter


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScoreInstance.objects.all()
    serializer_class = ScoreInstanceSerializer
    permission_classes = (permissions.AllowAny,)
    filter_class = ScoreFilter


class TestInstanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TestInstance.objects.all()
    serializer_class = TestInstanceSerializer
    permission_classes = (permissions.AllowAny,)
    filter_class = TestInstanceFilter


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

class ScoreClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScoreClass.objects.all()
    serializer_class = ScoreClassSerializer
    permission_classes = (permissions.AllowAny,)
    filter_fields = ('class_name',)
