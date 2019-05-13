import json
from datetime import date
from random import getrandbits as grb

from rest_framework import permissions, response, views, viewsets

from scidash.general.models import Tag
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


class TestInstanceCloneView(views.APIView):
    def get(self, request, test_id):
        test_pk = test_id

        try:
            test_instance = TestInstance.objects.get(pk=test_pk)
        except TestInstance.DoesNotExists:
            return response.Response(
                json.dumps(
                    {
                        'success': False,
                        'message': 'Test Instance not found'
                    }
                ), 404
            )

        new_test_instance = self.clone_test(test_instance, request)
        serializer = TestInstanceSerializer(new_test_instance)

        return response.Response(serializer.data)

    def clone_test(self, test_instance_model, request):
        test_pk = test_instance_model.pk
        test_instance_model.timestamp = date.today()
        test_instance_model.pk = None
        test_instance_model.hash_id = f"{grb(128)}_{grb(22)}"
        test_instance_model.owner = request.user

        test_instance_model.save()

        # Save required before to add the tags since the generic relation needs
        # the new key in order to clone the tags as well
        for tag in Tag.objects.filter(object_id=test_pk, content_type_id="11"):
            test_instance_model.tags.create(name=tag)

        return test_instance_model
