from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers, fields

from scidash.account.serializers import ScidashUserSerializer
from scidash.general.mixins import GetByKeyOrCreateMixin, GetOrCreateMixin
from scidash.general.serializers import TagSerializer, \
    SerializerWritableMethodField
from scidash.sciunitmodels.serializers import ModelInstanceSerializer
from scidash.sciunittests.validators import TestInstanceValidator
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
        fallback_observation_scheme = TestClass.objects.get(
            import_path=data.get('test_class').get('import_path')
        ).observation_schema

        try:
            TestInstanceValidator.validate(data, fallback_observation_scheme)
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
