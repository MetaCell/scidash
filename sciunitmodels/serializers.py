from drf_writable_nested import WritableNestedModelSerializer

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

    capabilities = CapabilitySerializer(many=True)

    class Meta:
        model = ModelClass
        fields = '__all__'


class ModelInstanceSerializer(WritableNestedModelSerializer):
    model_class = ModelClassSerializer()

    class Meta:
        model = ModelInstance
        fields = '__all__'
