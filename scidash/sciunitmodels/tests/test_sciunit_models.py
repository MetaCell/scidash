import json
import os

from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from scidash.general.models import ScidashUser
from scidash.sciunitmodels.serializers import ModelClassSerializer
from scidash.sciunittests.serializers import ScoreInstanceSerializer

SAMPLE_FILE = os.path.join(
    os.path.dirname(__file__), 'test_data/score_object.json'
)


class SciunitModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(SciunitModelTestCase, cls).setUpClass()

        factory = RequestFactory()
        request = factory.get('/data/upload/sample_json.json')
        cls.user = ScidashUser.objects.create_user(
            'admin', 'a@a.cc', 'montecarlo'
        )

        request.user = cls.user

        with open(SAMPLE_FILE) as f:
            score_serializer = ScoreInstanceSerializer(
                data=json.loads(f.read()), context={'request': request}
            )

        if score_serializer.is_valid():
            score_serializer.save()

    def scrub(self, obj, bad='_this_is_bad'):
        if isinstance(obj, dict):
            for k in list(obj):
                if k == bad:
                    del obj[k]
                else:
                    self.scrub(obj[k], bad)
        elif isinstance(obj, list):
            for i in reversed(range(len(obj))):
                if obj[i] == bad:
                    del obj[i]
                else:
                    self.scrub(obj[i], bad)
        else:
            pass

    def test_if_capabilities_endpoint_works_correctly(self):
        client = Client()
        response = client.get(reverse('capability-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()

        with open(SAMPLE_FILE) as f:
            data = json.loads(f.read())

        parsed_response = parsed_response.pop()
        self.scrub(parsed_response, 'id')
        capabilities_data = data.get('model_instance') \
            .get('model_class').get('capabilities').pop()

        for key in capabilities_data.keys():
            self.assertTrue(key in parsed_response)
            self.assertEqual(
                capabilities_data.get(key), parsed_response.get(key)
            )

    def test_if_model_class_endpoint_works_correctly(self):
        client = Client()
        response = client.get(reverse('model-class-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()

        with open(SAMPLE_FILE) as f:
            data = json.loads(f.read())

        parsed_response = parsed_response.pop()
        self.scrub(parsed_response, 'id')
        model_class_data = data.get('model_instance') \
            .get('model_class')

        for key in model_class_data.keys():
            self.assertTrue(key in parsed_response)
            self.assertEqual(
                model_class_data.get(key), parsed_response.get(key)
            )

    def test_if_model_instance_endpoint_works_correctly(self):
        client = Client()
        response = client.get(reverse('model-instance-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()

        with open(SAMPLE_FILE) as f:
            data = json.loads(f.read())

        parsed_response = parsed_response.pop()
        self.scrub(parsed_response, 'id')
        model_instance_data = data.get('model_instance')

        for key in model_instance_data.keys():
            self.assertTrue(key in parsed_response)
            self.assertEqual(
                model_instance_data.get(key), parsed_response.get(key)
            )


class SciunitModelMatchingClassObjects(TestCase):
    @classmethod
    def setUp(self):
        self.model_class = {
            "class_name": "ScoreModelClass",
            "capabilities": [{
                "class_name": "TestCapability"
            }],
            "import_path": "neuronunit.models.static.StaticModel",
            "url": "http://test-score.url"
        }

        self.user = ScidashUser.objects.create_user(
            'admin', 'a@a.cc', 'montecarlo'
        )

    def test_is_model_class_match_the_same_object(self):
        client = Client()
        client.force_login(self.user)

        model_class_serializer = ModelClassSerializer(data=self.model_class)

        if model_class_serializer.is_valid():
            model_class_serializer.save()

        response = client.get(reverse('model-class-list'))

        self.assertEqual(response.status_code, 200)
        parsed_response = response.json()

        self.assertEqual(len(parsed_response), 1)
