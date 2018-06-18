from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework_cache.registry import cache_registry
from rest_framework_cache.serializers import CachedSerializerMixin

from general.serializers import ScidashUserSerializer

from sciunittests.models import TestClass, TestSuite, TestInstance, \
                                ScoreInstance, ScoreClass
from sciunitmodels.serializers import ModelInstanceSerializer
from general.mixins import GetOrCreateMixin, GetByKeyOrCreateMixin


class TestSuiteSerializer(GetOrCreateMixin,
        WritableNestedModelSerializer,
        CachedSerializerMixin
        ):

    owner = ScidashUserSerializer(
            default=serializers.CurrentUserDefault(),
            read_only=True
            )

    class Meta:
        model = TestSuite
        fields = '__all__'


class TestClassSerializer(GetByKeyOrCreateMixin,
        WritableNestedModelSerializer,
        CachedSerializerMixin
        ):
    key = 'url'
    url = serializers.CharField(validators=[])

    class Meta:
        model = TestClass
        fields = '__all__'


class TestInstanceSerializer(GetByKeyOrCreateMixin,
        WritableNestedModelSerializer,
        CachedSerializerMixin
        ):
    test_suites = TestSuiteSerializer(many=True)
    test_class = TestClassSerializer()
    hash_id = serializers.CharField(validators=[])

    key = 'hash_id'

    class Meta:
        model = TestInstance
        fields = '__all__'


class ScoreClassSerializer(GetByKeyOrCreateMixin,
        WritableNestedModelSerializer,
        CachedSerializerMixin
        ):

    key = 'class_name'

    class Meta:
        model = ScoreClass
        fields = '__all__'


class ScoreInstanceSerializer(GetByKeyOrCreateMixin,
        WritableNestedModelSerializer,
        CachedSerializerMixin
        ):
    test_instance = TestInstanceSerializer()
    model_instance = ModelInstanceSerializer()
    score_class = ScoreClassSerializer()
    prediction = serializers.SerializerMethodField()
    hash_id = serializers.CharField(validators=[])
    owner = ScidashUserSerializer(
            default=serializers.CurrentUserDefault(),
            read_only=True
            )

    key = 'hash_id'

    def get_prediction(self, obj):
        if obj.prediction_numeric is not None:
            return obj.prediction_numeric

        return obj.prediction_dict

    def create(self, validated_data):
        prediction = self.initial_data.get('prediction')
        data = {}

        if isinstance(prediction, dict):
            data.update({
                'prediction_dict': prediction
                })
        else:
            data.update({
                'prediction_numeric': float(prediction)
                })

        validated_data.update(data)

        return super(ScoreInstanceSerializer, self).create(validated_data)

    class Meta:
        model = ScoreInstance
        exclude = ('prediction_dict', 'prediction_numeric', )


cache_registry.register(ScoreInstanceSerializer)
cache_registry.register(ScoreClassSerializer)
cache_registry.register(TestClassSerializer)
cache_registry.register(TestInstanceSerializer)
cache_registry.register(TestSuiteSerializer)
