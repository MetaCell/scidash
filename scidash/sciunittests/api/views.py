import json
from datetime import datetime as date
from random import getrandbits as grb

from rest_framework import permissions, response, views, viewsets
from django.db.models import Q
from django.conf import settings as s
from django.contrib.contenttypes.models import ContentType

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

    def filter_queryset(self, queryset):
        test_instance_content_type = ContentType.objects.get_for_model(
            TestInstance
        )

        TestInstance.objects.filter(test_class__import_path='').update(
            status=TestInstance.LOCKED
        )

        for instance in TestInstance.objects.filter(
            test_class__import_path=''
        ):
            Tag.objects.get_or_create(
                name=s.NO_IMPORT_TAG,
                content_type=test_instance_content_type,
                object_id=instance.pk
            )

        TestInstance.objects.filter(
            Q(score__isnull=True) & ~Q(test_class__import_path='')
        ).update(status=TestInstance.AVAILABLE)

        for instance in TestInstance.objects.filter(
            ~Q(test_class__import_path='')
        ):
            instance.tags.filter(name=s.NO_IMPORT_TAG).delete()

        return queryset


class TestSuiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializer
    permission_classes = (permissions.AllowAny, )
    filter_class = TestSuiteFilter


class TestClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TestClass.objects.filter(~Q(import_path=''))
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
        new_test_instance.timestamp = date.today()
        new_test_instance.save()
        serializer = TestInstanceSerializer(new_test_instance)

        return response.Response(serializer.data)

    def clone_test(self, test_instance_model, request):
        tags = [tag for tag in test_instance_model.tags.all()]
        test_instance_model.timestamp = date.today()
        test_instance_model.pk = None
        test_instance_model.hash_id = f"{grb(128)}_{grb(22)}"
        test_instance_model.owner = request.user
        test_instance_model.status = test_instance_model.AVAILABLE
        test_instance_model.save()

        # Save required before to add the tags since the generic relation needs
        # the new key in order to clone the tags as well
        for tag in tags:
            test_instance_model.tags.create(name=tag)

        return test_instance_model
