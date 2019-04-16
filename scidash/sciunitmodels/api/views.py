from random import getrandbits as grb
from datetime import date
import json
import pprint

from rest_framework import permissions, response, views, viewsets, mixins, generics

import scidash.sciunitmodels.helpers as hlp
from scidash.sciunitmodels.filters import ModelClassFilter, ModelInstanceFilter
from scidash.sciunitmodels.models import Capability, ModelClass, ModelInstance
from scidash.sciunitmodels.serializers import (
    CapabilitySerializer, ModelClassSerializer, ModelInstanceSerializer
)
from scidash.general.models import (
    Tag
)


class CapabilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Capability.objects.all()
    serializer_class = CapabilitySerializer
    permission_classes = (permissions.AllowAny, )


class ModelClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelClass.objects.all()
    serializer_class = ModelClassSerializer
    permission_classes = (permissions.AllowAny, )
    filter_class = ModelClassFilter


class ModelInstanceViewSet(viewsets.ModelViewSet):
    queryset = ModelInstance.objects.all()
    serializer_class = ModelInstanceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_class = ModelInstanceFilter


class ModelParametersView(views.APIView):
    def get(self, request):
        url = request.GET.get('model_url')
        error = None

        try:
            params = hlp.get_model_parameters(url)
        except Exception as e:
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
            return response.Response(json.dumps({
                'success': False,
                'message': 'model Instance not found'
            }), 404)

        new_model_instance = self.clone_model(model_instance)
        serializer = ModelInstanceSerializer(new_model_instance)
        return response.Response(serializer.data)

    def clone_model(self, model_instance_model):
        model_pk = model_instance_model.pk
        model_instance_model.timestamp = date.today()

        model_instance_model.pk = None
        model_instance_model.hash_id = f"{grb(128)}_{grb(22)}"
        model_instance_model.save()

        # Save required before to add the tags since the generic relation needs
        # the new key in order to clone the tags as well
        for tag in Tag.objects.filter(object_id=model_pk, content_type_id="8"):
            model_instance_model.tags.create(name=tag)

        return model_instance_model



class ModelInstanceEditView(views.APIView, mixins.UpdateModelMixin):

    def update(self, request, model_id):
        model_pk = model_id
        instance = ModelInstance.objects.get(pk=model_pk)
        instance.name = request.data.get("name")
        instance.save()

        try:
            error = None
            serializer = ModelInstanceSerializer(instance, data=request.data, context={'request': request})
            serializer.is_valid()
            self.perform_update(serializer)
        except Exception as e:
            error = e

        if error is None:
            return response.Response(serializer.data)
        else:
            return response.Response(
                {
                    'failed': True,
                    'message': str(error)
                }, 400
            )


    def put(self, request, model_id):
        return self.update(request, model_id)
