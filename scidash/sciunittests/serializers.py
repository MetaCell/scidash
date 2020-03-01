import json

import numpy as np
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers, fields

import sciunit
from scidash.account.serializers import ScidashUserSerializer
from scidash.general.helpers import import_class
from scidash.general.mixins import GetByKeyOrCreateMixin, GetOrCreateMixin
from scidash.general.serializers import TagSerializer, \
    SerializerWritableMethodField
from scidash.sciunitmodels.serializers import ModelInstanceSerializer
from scidash.sciunittests.helpers import build_destructured_unit
from scidash.sciunittests.models import (
    ScoreClass, ScoreInstance, TestClass, TestInstance, TestSuite
)


class TestSuiteSerializer(GetOrCreateMixin, WritableNestedModelSerializer):
    owner = ScidashUserSerializer(
        default=serializers.CurrentUserDefault(), read_only=True
    )

    class Meta:
        model = TestSuite
        fields = '__all__'


class TestClassSerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer):
    class_name = SerializerWritableMethodField(
        model_field=TestClass()._meta.get_field('class_name'))
    units_name = serializers.CharField(required=False)
    key = 'import_path'

    def get_class_name(self, obj):
        # return class_name + ( first part of import_path )
        return obj.class_name + (
            ' (' +
            '.'.join((obj.import_path if obj.import_path else ''
                      ).split('.')[0:-1]) + ')').replace(' ()', '')

    class Meta:
        model = TestClass
        fields = '__all__'


class TestInstanceSerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer
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
            if destructured.get('name', False):
                quantity = build_destructured_unit(destructured)
            else:
                quantity = destructured

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

        def process_obs(obs):
            try:
                obs = int(obs)
            except ValueError:
                obs = np.array(json.loads(obs))

            return obs

        if not isinstance(quantity, dict):
            obs_with_units = {
                x: (
                    process_obs(y) * quantity
                    if x not in without_units else process_obs(y)
                )
                for x, y in observations.items()
            }
        else:
            obs_with_units = {
                x: (
                    process_obs(y) * import_class(quantity[x])
                    if x not in without_units else process_obs(y)
                )
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
    GetByKeyOrCreateMixin, WritableNestedModelSerializer
):
    key = 'class_name'

    class Meta:
        model = ScoreClass
        fields = '__all__'


class ScoreInstanceSerializer(
    GetByKeyOrCreateMixin, WritableNestedModelSerializer
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
