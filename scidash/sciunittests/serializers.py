from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_cache.registry import cache_registry
from rest_framework_cache.serializers import CachedSerializerMixin

from scidash.account.serializers import ScidashUserSerializer
from scidash.general.mixins import GetByKeyOrCreateMixin, GetOrCreateMixin
from scidash.general.serializers import TagSerializer
from scidash.sciunitmodels.serializers import ModelInstanceSerializer
from scidash.general.helpers import import_class
from scidash.sciunittests.models import (
    ScoreClass, ScoreInstance, TestClass, TestInstance, TestSuite
)
import sciunit


class TestSuiteSerializer(
    GetOrCreateMixin, WritableNestedModelSerializer, CachedSerializerMixin
):

    owner = ScidashUserSerializer(
        default=serializers.CurrentUserDefault(), read_only=True
    )

    class Meta:
        model = TestSuite
        fields = '__all__'


class TestClassSerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer, CachedSerializerMixin
):
    key = 'url'
    url = serializers.CharField(validators=[])

    class Meta:
        model = TestClass
        fields = '__all__'


class TestInstanceSerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer, CachedSerializerMixin
):
    test_suites = TestSuiteSerializer(many=True, required=False)
    test_class = TestClassSerializer()
    hash_id = serializers.CharField(validators=[])
    tags = TagSerializer(many=True, required=False)
    owner = ScidashUserSerializer(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    tags = TagSerializer(many=True, required=False)

    key = 'hash_id'

    def leave_it_for_later(self, data):
        sciunit.settings['PREVALIDATE'] = True

        class_data = data.get('test_class')
        test_class = import_class(class_data.get('import_path'))
        quantity = import_class(class_data.get('units'))
        observations = data.get('observation')
        without_units = []

        def filter_units(schema):
            result = []
            for key, rules in schema.items():
                if rules.get('units', False):
                    result.append(key)

            return result

        if isinstance(test_class.observations_schema, list):
            for schema in test_class.observation_schema:
                without_units += filter_units(schema)
        else:
            without_units = filter_units(test_class.observation_schema)

        obs_with_units = {x: int(y)*quantity for x, y in observations.items()}

        try:
            test_class(obs_with_units)
        except Exception as e:
            raise serializers.ValidationError(e)

        return data

    class Meta:
        model = TestInstance
        fields = '__all__'


class ScoreClassSerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer, CachedSerializerMixin
):

    key = 'class_name'

    class Meta:
        model = ScoreClass
        fields = '__all__'


class ScoreInstanceSerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer, CachedSerializerMixin
):
    test_instance = TestInstanceSerializer()
    model_instance = ModelInstanceSerializer()
    score_class = ScoreClassSerializer()
    prediction = serializers.SerializerMethodField()
    hash_id = serializers.CharField(validators=[])
    owner = ScidashUserSerializer(
        default=serializers.CurrentUserDefault(), read_only=True
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
            data.update({'prediction_dict': prediction})
        else:
            data.update({'prediction_numeric': float(prediction)})

        validated_data.update(data)

        return super(ScoreInstanceSerializer, self).create(validated_data)

    class Meta:
        model = ScoreInstance
        exclude = (
            'prediction_dict',
            'prediction_numeric',
        )


cache_registry.register(ScoreInstanceSerializer)
cache_registry.register(ScoreClassSerializer)
cache_registry.register(TestClassSerializer)
cache_registry.register(TestInstanceSerializer)
cache_registry.register(TestSuiteSerializer)
