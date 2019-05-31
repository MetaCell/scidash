import json
import logging
from datetime import date
from random import getrandbits as grb

from rest_framework import (
    mixins, permissions, response, views, viewsets
)

import scidash.sciunitmodels.helpers as hlp
from scidash.general.models import Tag
from scidash.sciunitmodels.filters import ModelClassFilter, ModelInstanceFilter
from scidash.sciunitmodels.models import Capability, ModelClass, ModelInstance
from scidash.sciunitmodels.serializers import (
    CapabilitySerializer, ModelClassSerializer, ModelInstanceSerializer
)

logger = logging.getLogger('db')


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
        if "githubusercontent" not in url and "github" in url:
            string1 = url[0 : url.index("/blob/")]
            string2 = url[(url.index("/blob/") + 5) : len(url)]
            github_user = string1[(string1[0 : string1.rfind("/")].rfind("/") + 1) : string1.rfind("/")]
            repository = string1[(string1.rfind("/") + 1) : len(string1)]
            url = "https://raw.githubusercontent.com/" + github_user + "/" + repository + string2
        error = None

        try:
            params = hlp.get_model_parameters(url)
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

<<<<<<< HEAD
    def clone_model(self, model_instance_model, request):
=======
    def clone_model(self, model_instance_model):
>>>>>>> 4b05ab6990edb7a552bcf6e913f534758869c072
        tags = [tag for tag in model_instance_model.tags.all()]
        model_instance_model.timestamp = date.today()

        model_instance_model.pk = None
        model_instance_model.hash_id = f"{grb(128)}_{grb(22)}"
        model_instance_model.owner = request.user
        model_instance_model.save()

        # Save required before to add the tags since the generic relation needs
        # the new key in order to clone the tags as well
        for tag in tags:
            model_instance_model.tags.create(name=tag)

        return model_instance_model
