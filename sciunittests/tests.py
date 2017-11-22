import os
import json

from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from general.models import ScidashUser

from sciunittests.serializers import ScoreSerializer

SAMPLE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),
        'json_sample.json')


class SciunitTestTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SciunitTestTestCase, cls).setUpClass()

        factory = RequestFactory()
        request = factory.get('/data/upload/sample_json.json')
        cls.user = ScidashUser.objects.create_user('admin', 'a@a.cc',
                'montecarlo')

        request.user = cls.user

        with open(SAMPLE_FILE) as f:
            score_serializer = ScoreSerializer(data=json.loads(f.read()),
                    context={'request': request})

        if score_serializer.is_valid():
            score_serializer.save()
        else:
            print(score_serializer.errors)

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

    def test_if_scores_endpoint_works_correctly(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('score-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()

        with open(SAMPLE_FILE) as f:
            data = json.loads(f.read())

        parsed_response = parsed_response.pop()
        self.scrub(parsed_response, 'id')
        self.scrub(parsed_response, 'timestamp')
        parsed_keys = parsed_response.keys()

        for key in data.keys():
            self.assertTrue(key in parsed_keys)
            self.assertEqual(data.get(key), parsed_response.get(key))

    def test_if_test_instance_endpoint_works_correctly(self):
        client = Client()
        client.force_login(user=self.user)
        response = client.get(reverse('test-instance-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()

        with open(SAMPLE_FILE) as f:
            data = json.loads(f.read())

        parsed_response = parsed_response.pop()
        self.scrub(parsed_response, 'id')
        self.scrub(parsed_response, 'timestamp')
        parsed_keys = parsed_response.keys()
        test_instance_data = data.get('test_instance')

        for key in data.get('test_instance').keys():
            self.assertTrue(key in parsed_keys)
            self.assertEqual(test_instance_data.get(key),
                    parsed_response.get(key))

    def test_if_test_class_endpoint_works_correctly(self):
        client = Client()
        client.force_login(user=self.user)
        response = client.get(reverse('test-class-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()

        with open(SAMPLE_FILE) as f:
            data = json.loads(f.read())

        parsed_response = parsed_response.pop()
        self.scrub(parsed_response, 'id')
        self.scrub(parsed_response, 'timestamp')
        parsed_keys = parsed_response.keys()
        test_classes_data = data.get('test_instance').get('test_class')

        for key in data.get('test_instance').get('test_class').keys():
            self.assertTrue(key in parsed_keys)
            self.assertEqual(test_classes_data.get(key),
                    parsed_response.get(key))

    def test_if_test_suite_endpoint_works_correctly(self):
        client = Client()
        client.force_login(user=self.user)
        response = client.get(reverse('test-suite-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()

        with open(SAMPLE_FILE) as f:
            data = json.loads(f.read())

        parsed_response = parsed_response.pop()
        self.scrub(parsed_response, 'id')
        self.scrub(parsed_response, 'timestamp')
        parsed_keys = parsed_response.keys()
        test_classes_data = data.get('test_instance').get('test_suites').pop()

        for key in test_classes_data:
            self.assertTrue(key in parsed_keys)
            self.assertEqual(test_classes_data.get(key),
                    parsed_response.get(key))
