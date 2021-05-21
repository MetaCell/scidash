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
        try:
            # old style
            sciunit.settings['PREVALIDATE'] = True
        except:
            # new style
            try:
                sciunit.config_set('PREVALIDATE', True)
            except:
                sciunit.config.set('PREVALIDATE', True)

        class_data = data.get('test_class')

        if not class_data.get('import_path', False):
            return data

        test_class = import_class(class_data.get('import_path'))

        if class_data.get("units"):
            try:
                destructured = json.loads(class_data.get('units'))
            except json.JSONDecodeError:
                quantity = import_class(class_data.get('units'))
            else:
                if destructured.get('name', False):
                    quantity = build_destructured_unit(destructured)
                else:
                    quantity = destructured
        else:
            quantity = 1

        observations = data.get('observation')
        without_units = []

        def filter_units(schema):
            result = []
            for key, rules in schema.items():
                if not rules.get('units', False):
                    result.append(key)

            return result

        observation_schema = test_class.observation_schema
        if not observation_schema:
            observation_schema = class_data.get("observation_schema")
            if not observation_schema:
                observation_schema = TestClass.objects.get(import_path=class_data.get('import_path')).observation_schema
        if isinstance(observation_schema, list):
            for schema in observation_schema:
                if isinstance(schema, tuple) or len(schema)>1:
                    without_units += filter_units(schema[1])
                else:
                    without_units += filter_units(schema)
        elif observation_schema:
            without_units = filter_units(observation_schema)

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
    def create(self, validated_data):
        model = self.Meta.model
        relations, reverse_relations = self._extract_relations(validated_data)

        self.update_or_create_direct_relations(
            validated_data,
            relations,
        )

        key_url = validated_data.get("url")
        key_class_name = validated_data.get("class_name")

        if key_url != "" and key_class_name != "":
            try:
                model_instance = model.objects.get(**{"url": key_url, "class_name": key_class_name})
                instance = super(GetByKeyOrCreateMixin,
                                 self).update(model_instance, validated_data)
            except model.DoesNotExist:
                instance = super(GetByKeyOrCreateMixin,
                                 self).create(validated_data)
        else:
            if not validated_data.get('id', False):
                instance = super(GetByKeyOrCreateMixin,
                                 self).create(validated_data)
            else:
                model_instance = model.objects.get(pk=validated_data.get('id'))
                instance = super(GetByKeyOrCreateMixin,
                                 self).update(model_instance, validated_data)

        self.update_or_create_reverse_relations(instance, reverse_relations)

        return instance

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
