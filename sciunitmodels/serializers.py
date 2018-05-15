from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from sciunitmodels.models import Capability, ModelClass, ModelInstance
from general.mixins import GetByKeyOrCreateMixin


class CapabilitySerializer(GetByKeyOrCreateMixin,
        WritableNestedModelSerializer):

    key = 'class_name'

    class Meta:
        model = Capability
        fields = '__all__'


class ModelClassSerializer(GetByKeyOrCreateMixin,
        WritableNestedModelSerializer):
    key = 'url'
    url = serializers.CharField(validators=[])

    capabilities = CapabilitySerializer(many=True)

    class Meta:
        model = ModelClass
        fields = '__all__'


class ModelInstanceSerializer(GetByKeyOrCreateMixin,
        WritableNestedModelSerializer):
    model_class = ModelClassSerializer()
    hash_id = serializers.CharField(validators=[])

    key = 'hash_id'

    class Meta:
        model = ModelInstance
        fields = '__all__'
