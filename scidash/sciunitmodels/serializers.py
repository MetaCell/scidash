from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from scidash.account.serializers import ScidashUserSerializer
from scidash.general.mixins import GetByKeyOrCreateMixin
from scidash.general.serializers import TagSerializer
from scidash.sciunitmodels.models import Capability, ModelClass, ModelInstance


class CapabilitySerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer
):

    key = 'class_name'

    class Meta:
        model = Capability
        fields = '__all__'


class ModelClassSerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer
):
    key = 'import_path'
    capabilities = CapabilitySerializer(many=True)
    url = serializers.URLField(
        allow_null=True, allow_blank=True, validators=[]
    )

    class Meta:
        model = ModelClass
        fields = '__all__'


class ModelInstanceSerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer
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
