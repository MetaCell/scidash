from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from general.serializers import ScidashUserSerializer

from sciunittests.models import TestClass, TestSuite, TestInstance, Score
from sciunitmodels.serializers import ModelInstanceSerializer


class TestSuiteSerializer(WritableNestedModelSerializer):
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
    owner = ScidashUserSerializer(
            default=serializers.CurrentUserDefault(),
            read_only=True
            )

    class Meta:
        model = Score
        fields = '__all__'
