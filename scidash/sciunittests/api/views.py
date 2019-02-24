from rest_framework import permissions, viewsets

from scidash.sciunittests.filters import (
    ScoreFilter, TestInstanceFilter, TestSuiteFilter
)
from scidash.sciunittests.models import (
    ScoreClass, ScoreInstance, TestClass, TestInstance, TestSuite
)
from scidash.sciunittests.serializers import (
    ScoreClassSerializer, ScoreInstanceSerializer, TestClassSerializer,
    TestInstanceSerializer, TestSuiteSerializer
)


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScoreInstance.objects.all()
    serializer_class = ScoreInstanceSerializer
    permission_classes = (permissions.AllowAny, )
    filter_class = ScoreFilter


class TestInstanceViewSet(viewsets.ModelViewSet):
    queryset = TestInstance.objects.all()
    serializer_class = TestInstanceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_class = TestInstanceFilter


class TestSuiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializer
    permission_classes = (permissions.AllowAny, )
    filter_class = TestSuiteFilter


class TestClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TestClass.objects.all()
    serializer_class = TestClassSerializer
    permission_classes = (permissions.AllowAny, )
    filter_fields = ('class_name', )


class ScoreClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScoreClass.objects.all()
    serializer_class = ScoreClassSerializer
    permission_classes = (permissions.AllowAny, )
    filter_fields = ('class_name', )
