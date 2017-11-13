from drf_writable_nested import WritableNestedModelSerializer

from sciunittests.models import TestClass, TestSuite, TestInstance, Score
from sciunitmodels.serializers import ModelInstanceSerializer


class TestSuiteSerializer(WritableNestedModelSerializer):

    class Meta:
        model = TestSuite
        fields = '__all__'


class TestClassSerializer(WritableNestedModelSerializer):

    class Meta:
        model = TestClass
        fields = '__all__'


class TestInstanceSerializer(WritableNestedModelSerializer):
    test_suite = TestSuiteSerializer()
    test_class = TestClassSerializer()

    class Meta:
        model = TestInstance
        fields = '__all__'


class ScoreSerializer(WritableNestedModelSerializer):
    test_instance = TestInstanceSerializer()
    model_instance = ModelInstanceSerializer()

    class Meta:
        model = Score
        fields = '__all__'
