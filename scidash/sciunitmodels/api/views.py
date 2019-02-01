from rest_framework import permissions, viewsets

from scidash.sciunitmodels.filters import ModelInstanceFilter
from scidash.sciunitmodels.models import Capability, ModelClass, ModelInstance
from scidash.sciunitmodels.serializers import (
    CapabilitySerializer, ModelClassSerializer, ModelInstanceSerializer
)


class CapabilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Capability.objects.all()
    serializer_class = CapabilitySerializer
    permission_classes = (permissions.AllowAny, )


class ModelClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelClass.objects.all()
    serializer_class = ModelClassSerializer
    permission_classes = (permissions.AllowAny, )


class ModelInstanceViewSet(viewsets.ModelViewSet):
    queryset = ModelInstance.objects.all()
    serializer_class = ModelInstanceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_class = ModelInstanceFilter
