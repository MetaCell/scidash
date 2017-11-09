from rest_framework import serializers

from sciunitmodels.models import Capability, ModelClass, ModelInstance


class CapabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Capability


class ModelClassSerializer(serializers.Serializer):
    capabilities = CapabilitySerializer(many=True)

    class Meta:
        model = ModelClass


class ModelInstanceSerializer(serializers.Serializer):
    model_class = ModelClassSerializer()

    class Meta:
        model = ModelInstance
