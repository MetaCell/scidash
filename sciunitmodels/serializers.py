from drf_writable_nested import WritableNestedModelSerializer

from sciunitmodels.models import Capability, ModelClass, ModelInstance


class CapabilitySerializer(WritableNestedModelSerializer):

    class Meta:
        model = Capability
        fields = '__all__'


class ModelClassSerializer(WritableNestedModelSerializer):
    capabilities = CapabilitySerializer(many=True)

    class Meta:
        model = ModelClass
        fields = '__all__'


class ModelInstanceSerializer(WritableNestedModelSerializer):
    model_class = ModelClassSerializer()

    class Meta:
        model = ModelInstance
        fields = '__all__'
