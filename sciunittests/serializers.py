from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from general.serializers import ScidashUserSerializer

from sciunittests.models import TestClass, TestSuite, TestInstance, \
                                ScoreInstance, ScoreClass
from sciunitmodels.serializers import ModelInstanceSerializer
from general.mixins import GetOrCreateMixin, GetByKeyOrCreateMixin


class TestSuiteSerializer(GetOrCreateMixin,
        WritableNestedModelSerializer):

    owner = ScidashUserSerializer(
            default=serializers.CurrentUserDefault(),
            read_only=True
            )

    class Meta:
        model = TestSuite
        fields = '__all__'


class TestClassSerializer(GetByKeyOrCreateMixin,
        WritableNestedModelSerializer):
    key = 'url'
    url = serializers.CharField(validators=[])

    class Meta:
        model = TestClass
        fields = '__all__'


class TestInstanceSerializer(GetByKeyOrCreateMixin,
        WritableNestedModelSerializer):
    test_suites = TestSuiteSerializer(many=True)
    test_class = TestClassSerializer()
    hash_id = serializers.CharField(validators=[])

    key = 'hash_id'

    class Meta:
        model = TestInstance
        fields = '__all__'


class ScoreClassSerializer(GetByKeyOrCreateMixin,
        WritableNestedModelSerializer):

    key = 'class_name'

    class Meta:
        model = ScoreClass
        fields = '__all__'


class ScoreInstanceSerializer(GetByKeyOrCreateMixin,
        WritableNestedModelSerializer):
    test_instance = TestInstanceSerializer()
    model_instance = ModelInstanceSerializer()
    score_class = ScoreClassSerializer()
    prediction = serializers.SerializerMethodField()
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
