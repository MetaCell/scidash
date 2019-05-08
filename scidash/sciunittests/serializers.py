import json

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_cache.registry import cache_registry
from rest_framework_cache.serializers import CachedSerializerMixin

import sciunit
from scidash.account.serializers import ScidashUserSerializer
from scidash.general.helpers import import_class
from scidash.general.mixins import GetByKeyOrCreateMixin, GetOrCreateMixin
from scidash.general.serializers import TagSerializer
from scidash.sciunitmodels.serializers import ModelInstanceSerializer
from scidash.sciunittests.helpers import build_destructured_unit
from scidash.sciunittests.models import (
    ScoreClass, ScoreInstance, TestClass, TestInstance, TestSuite
)


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
    units_name = serializers.CharField(required=False)
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
    key = 'hash_id'

    def validate(self, data):
        sciunit.settings['PREVALIDATE'] = True


        class_data = data.get('test_class')

        if not class_data.get('import_path', False):
            return data

        test_class = import_class(class_data.get('import_path'))

        try:
            destructured = json.loads(class_data.get('units'))
        except json.JSONDecodeError:
            quantity = import_class(class_data.get('units'))
        else:
            quantity = build_destructured_unit(destructured)

        observations = data.get('observation')
        without_units = []

        def filter_units(schema):
            result = []
            for key, rules in schema.items():
                if not rules.get('units', False):
                    result.append(key)

            return result

        if isinstance(test_class.observation_schema, list):
            for schema in test_class.observation_schema:
                if isinstance(schema, tuple):
                    without_units += filter_units(schema[1])
                else:
                    without_units += filter_units(schema)
        else:
            without_units = filter_units(test_class.observation_schema)

        obs_with_units = {
            x: (int(y) * quantity if x not in without_units else int(y))
            for x, y in observations.items()
        }

        try:
            test_class(obs_with_units)
        except Exception as e:
            raise serializers.ValidationError(
                f"Can't instantiate class, reason candidates: {e}"
            )

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
