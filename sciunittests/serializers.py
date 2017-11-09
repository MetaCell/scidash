from rest_framework import serializers

from sciunittests.models import TestClass, TestSuite, TestInstance, Score
from sciunitmodels.serializers import ModelInstanceSerializer


class TestSuiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestSuite
        fields = '__all__'


class TestClassSerializer(serializers.Serializer):

    class Meta:
        model = TestClass
        fields = '__all__'


class TestInstanceSerializer(serializers.Serializer):
    test_suite = TestSuiteSerializer()
    test_class = TestClassSerializer()

    class Meta:
        model = TestInstance
        fields = '__all__'


class ScoreSerializer(serializers.Serializer):
    test_instance = TestInstanceSerializer()
    model_instance = ModelInstanceSerializer()


    class Meta:
        model = Score
        fields = '__all__'
