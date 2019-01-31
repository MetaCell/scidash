from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_cache.registry import cache_registry
from rest_framework_cache.serializers import CachedSerializerMixin

from scidash.general.mixins import GetByKeyOrCreateMixin
from scidash.general.serializers import TagSerializer
from scidash.sciunitmodels.models import Capability, ModelClass, ModelInstance
from scidash.account.serializers import ScidashUserSerializer


class CapabilitySerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer, CachedSerializerMixin
):

    key = 'class_name'

    class Meta:
        model = Capability
        fields = '__all__'


class ModelClassSerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer, CachedSerializerMixin
):
    key = 'url'
    url = serializers.CharField(validators=[])

    capabilities = CapabilitySerializer(many=True)

    class Meta:
        model = ModelClass
        fields = '__all__'


class ModelInstanceSerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer, CachedSerializerMixin
):
    model_class = ModelClassSerializer()
    hash_id = serializers.CharField(validators=[])
    tags = TagSerializer(many=True, required=False)
    owner = ScidashUserSerializer(
        default=serializers.CurrentUserDefault(), read_only=True
    )


    key = 'hash_id'

    class Meta:
        model = ModelInstance
        fields = '__all__'


cache_registry.register(CapabilitySerializer)
cache_registry.register(ModelClassSerializer)
cache_registry.register(ModelInstanceSerializer)
