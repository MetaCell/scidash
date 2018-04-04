from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from general.serializers import ScidashUserSerializer

from sciunittests.models import TestClass, TestSuite, TestInstance, Score
from sciunitmodels.serializers import ModelInstanceSerializer
from general.mixins import GetByHashOrCreateMixin


class TestSuiteSerializer(GetByHashOrCreateMixin,
        WritableNestedModelSerializer):

    owner = ScidashUserSerializer(
            default=serializers.CurrentUserDefault(),
            read_only=True
            )

    class Meta:
        model = TestSuite
        fields = '__all__'


class TestClassSerializer(WritableNestedModelSerializer):

    class Meta:
        model = TestClass
        fields = '__all__'


class TestInstanceSerializer(WritableNestedModelSerializer):
    test_suites = TestSuiteSerializer(many=True)
    test_class = TestClassSerializer()

    class Meta:
        model = TestInstance
        fields = '__all__'


class ScoreSerializer(WritableNestedModelSerializer):
    test_instance = TestInstanceSerializer()
    model_instance = ModelInstanceSerializer()
    prediction = serializers.SerializerMethodField()
    owner = ScidashUserSerializer(
            default=serializers.CurrentUserDefault(),
            read_only=True
            )

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

        return super(ScoreSerializer, self).create(validated_data)

    class Meta:
        model = Score
        exclude = ('prediction_dict', 'prediction_numeric', )
