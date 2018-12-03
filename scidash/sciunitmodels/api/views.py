from rest_framework import viewsets, permissions

from scidash.sciunitmodels.serializers import CapabilitySerializer, \
        ModelClassSerializer, \
        ModelInstanceSerializer

from scidash.sciunitmodels.models import Capability, ModelClass, ModelInstance


class CapabilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Capability.objects.all()
    serializer_class = CapabilitySerializer
    permission_classes = (permissions.AllowAny,)


class ModelClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelClass.objects.all()
    serializer_class = ModelClassSerializer
    permission_classes = (permissions.AllowAny,)


class ModelInstanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelInstance.objects.all()
    serializer_class = ModelInstanceSerializer
    permission_classes = (permissions.AllowAny,)
