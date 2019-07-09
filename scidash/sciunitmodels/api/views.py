import json
import logging
from datetime import date
from random import getrandbits as grb

from rest_framework import permissions, response, views, viewsets
from django.db.models import Q
from django.conf import settings as s
from django.contrib.contenttypes.models import ContentType

import scidash.sciunitmodels.helpers as hlp
from scidash.sciunitmodels.filters import ModelClassFilter, ModelInstanceFilter
from scidash.sciunitmodels.models import Capability, ModelClass, ModelInstance
from pygeppetto_gateway.interpreters.helpers import URLProcessor
from scidash.general.models import Tag
from scidash.sciunitmodels.serializers import (
    CapabilitySerializer, ModelClassSerializer, ModelInstanceSerializer
)

logger = logging.getLogger('db')


class CapabilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Capability.objects.all()
    serializer_class = CapabilitySerializer
    permission_classes = (permissions.AllowAny, )


class ModelClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelClass.objects.filter(~Q(import_path=''))
    serializer_class = ModelClassSerializer
    permission_classes = (permissions.AllowAny, )
    filter_class = ModelClassFilter


class ModelInstanceViewSet(viewsets.ModelViewSet):
    queryset = ModelInstance.objects.all()
    serializer_class = ModelInstanceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_class = ModelInstanceFilter

    def filter_queryset(self, queryset):
        model_instance_content_type = ContentType.objects.get_for_model(
            ModelInstance
        )

        ModelInstance.objects.filter(model_class__import_path='').update(
            status=ModelInstance.LOCKED
        )

        for instance in ModelInstance.objects.filter(
            model_class__import_path=''
        ):
            Tag.objects.get_or_create(
                name=s.NO_IMPORT_TAG,
                content_type=model_instance_content_type,
                object_id=instance.pk
            )

        ModelInstance.objects.filter(
            Q(score__isnull=True) & ~Q(model_class__import_path='')
        ).update(status=ModelInstance.AVAILABLE)

        for instance in ModelInstance.objects.filter(
            ~Q(model_class__import_path='')
        ):
            instance.tags.filter(name=s.NO_IMPORT_TAG).delete()

        return queryset


class ModelParametersView(views.APIView):
    def get(self, request):
        processor = URLProcessor(request.GET.get('model_url'))
        url = processor.get_file_url()

        error = None

        try:
            params = hlp.get_model_parameters(url, processor.model_id)
        except Exception as e:
            logger.exception(e)
            error = e

        if error is None:
            return response.Response(params)
        else:
            return response.Response(
                {
                    'failed': True,
                    'message': str(error)
                }, 400
            )


class ModelInstanceCloneView(views.APIView):
    def get(self, request, model_id):
        model_pk = model_id

        try:
            model_instance = ModelInstance.objects.get(pk=model_pk)
        except ModelInstance.DoesNotExists:
            return response.Response(
                json.dumps(
                    {
                        'success': False,
                        'message': 'model Instance not found'
                    }
                ), 404
            )

        new_model_instance = self.clone_model(model_instance, request)
        serializer = ModelInstanceSerializer(new_model_instance)
        return response.Response(serializer.data)

    def clone_model(self, model_instance_model, request):
        tags = [tag for tag in model_instance_model.tags.all()]
        model_instance_model.timestamp = date.today()

        model_instance_model.pk = None
        model_instance_model.hash_id = f"{grb(128)}_{grb(22)}"
        model_instance_model.owner = request.user
        model_instance_model.status = model_instance_model.AVAILABLE
        model_instance_model.save()

        # Save required before to add the tags since the generic relation needs
        # the new key in order to clone the tags as well
        for tag in tags:
            model_instance_model.tags.create(name=tag)

        return model_instance_model
