import os
import json
from datetime import timedelta

from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from general.models import ScidashUser

from sciunittests.serializers import ScoreSerializer
from sciunittests.models import Score

SAMPLE_OBJECT = os.path.join(os.path.dirname(os.path.dirname(__file__)),
        'test_data/score_object.json')

SAMPLE_OBJECT_LIST = os.path.join(os.path.dirname(os.path.dirname(__file__)),
        'test_data/score_objects_list.json')


class SciunitTestTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SciunitTestTestCase, cls).setUpClass()

        factory = RequestFactory()
        request = factory.get('/data/upload/score_object.json')
        cls.user = ScidashUser.objects.create_user('admin', 'a@a.cc',
                'montecarlo')

        request.user = cls.user

        with open(SAMPLE_OBJECT) as f:
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

        with open(SAMPLE_OBJECT) as f:
            data = json.loads(f.read())

        parsed_response = parsed_response.pop()
        self.scrub(parsed_response, 'id')
        self.scrub(parsed_response, 'timestamp')
        self.scrub(parsed_response, 'owner')
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

        with open(SAMPLE_OBJECT) as f:
            data = json.loads(f.read())

        parsed_response = parsed_response.pop()
        self.scrub(parsed_response, 'id')
        self.scrub(parsed_response, 'timestamp')
        self.scrub(parsed_response, 'owner')
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

        with open(SAMPLE_OBJECT) as f:
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

        with open(SAMPLE_OBJECT) as f:
            data = json.loads(f.read())

        parsed_response = parsed_response.pop()
        self.scrub(parsed_response, 'id')
        self.scrub(parsed_response, 'timestamp')
        self.scrub(parsed_response, 'owner')
        parsed_keys = parsed_response.keys()
        test_classes_data = data.get('test_instance').get('test_suites').pop()

        for key in test_classes_data:
            self.assertTrue(key in parsed_keys)
            self.assertEqual(test_classes_data.get(key),
                    parsed_response.get(key))


class SciunitTestFiltersScoreTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SciunitTestFiltersScoreTestCase, cls).setUpClass()

        factory = RequestFactory()
        request = factory.get('/data/upload/score_object_list.json')
        cls.user = ScidashUser.objects.create_user('admin', 'a@a.cc',
                'montecarlo')

        request.user = cls.user

        with open(SAMPLE_OBJECT_LIST) as f:
            objects_list = json.loads(f.read())

        for item in objects_list:
            score_serializer = ScoreSerializer(data=item,
                    context={'request': request})

            if score_serializer.is_valid():
                score_serializer.save()
            else:
                print(score_serializer.errors)

    def test_scores_endpoint_filters_get_by_id(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('score-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()
        first_element = parsed_response[0]
        first_element_id = first_element.get('id')

        response = client.get(reverse('score-detail', kwargs={
            'pk': first_element_id
            }))

        parsed_response = response.json()
        self.assertEqual(first_element, parsed_response)

    def test_scores_endpoint_filters_get_by_owner(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('score-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()
        first_element = parsed_response[0]
        owner = first_element.get('owner')
        owner_id = owner.get('id')

        filtered_url = '{}?owner={}'.format(reverse('score-list'), owner_id)

        response = client.get(filtered_url)

        parsed_response = response.json()

        for item in parsed_response:
            self.assertEqual(item.get('owner').get('id'), owner_id)

    def test_scores_endpoint_filters_get_by_class_name(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('score-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()
        first_element = parsed_response[0]
        model_class_name = first_element.get('model_instance') \
                                        .get('model_class').get('class_name')

        filtered_url = '{}?model_instance__model_class__class_name={}'.format(
                reverse('score-list'),
                model_class_name
                )

        response = client.get(filtered_url)

        parsed_response = response.json()

        self.assertEqual(len(parsed_response), 1)
        self.assertEqual(first_element, parsed_response[0])

    def test_scores_endpoint_filters_get_by_instance_id(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('score-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()
        first_element = parsed_response[0]
        model_instance_id = first_element.get('model_instance').get('id')

        filtered_url = '{}?model_instance={}'.format(
                reverse('score-list'),
                model_instance_id
                )

        response = client.get(filtered_url)

        parsed_response = response.json()

        self.assertEqual(len(parsed_response), 1)
        self.assertEqual(first_element, parsed_response[0])

    def test_scores_endpoint_filters_get_by_timestamp(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('score-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()
        first_element = parsed_response[0]

        timestamp = Score.objects.get(pk=first_element.get('id')).timestamp

        filtered_url = '{}?timestamp_before={}'.format(
                reverse('score-list'),
                (timestamp - timedelta(1)).isoformat()
                )

        response = client.get(filtered_url)
        parsed_response = response.json()
        self.assertEqual(len(parsed_response), 0)

        filtered_url = '{}?timestamp_after={}'.format(
                reverse('score-list'),
                (timestamp + timedelta(1)).isoformat()
                )

        response = client.get(filtered_url)
        parsed_response = response.json()
        self.assertEqual(len(parsed_response), 0)

        filtered_url = '{}?timestamp_after={}&timestamp_before={}'.format(
                reverse('score-list'),
                (timestamp - timedelta(0, 3600)).isoformat(),
                (timestamp + timedelta(0, 3600)).isoformat()
                )

        response = client.get(filtered_url)
        parsed_response = response.json()

        self.assertTrue(len(parsed_response) > 1)


class SciunitTestFiltersTestSuiteTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SciunitTestFiltersTestSuiteTestCase, cls).setUpClass()

        factory = RequestFactory()
        request = factory.get('/data/upload/score_object_list.json')
        cls.user = ScidashUser.objects.create_user('admin', 'a@a.cc',
                'montecarlo')

        request.user = cls.user

        with open(SAMPLE_OBJECT_LIST) as f:
            objects_list = json.loads(f.read())

        for item in objects_list:
            score_serializer = ScoreSerializer(data=item,
                    context={'request': request})

            if score_serializer.is_valid():
                score_serializer.save()
            else:
                print(score_serializer.errors)

    def test_test_suite_endpoint_filters_get_by_id(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('test-suite-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()
        first_element = parsed_response[0]
        first_element_id = first_element.get('id')

        response = client.get(reverse('test-suite-detail', kwargs={
            'pk': first_element_id
            }))

        parsed_response = response.json()
        self.assertEqual(first_element, parsed_response)

    def test_test_suite_endpoint_filters_get_by_owner(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('test-suite-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()
        first_element = parsed_response[0]
        owner = first_element.get('owner')
        owner_id = owner.get('id')

        filtered_url = '{}?owner={}'.format(reverse('test-suite-list'), owner_id)

        response = client.get(filtered_url)

        parsed_response = response.json()

        for item in parsed_response:
            self.assertEqual(item.get('owner').get('id'), owner_id)

    def test_test_suite_endpoint_filters_get_by_timestamp(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('test-suite-list'))

        self.assertEqual(response.status_code, 200)

        parsed_response = response.json()
        first_element = parsed_response[0]

        timestamp = Score.objects.get(pk=first_element.get('id')).timestamp

        filtered_url = '{}?timestamp_before={}'.format(
                reverse('test-suite-list'),
                (timestamp - timedelta(1)).isoformat()
                )

        response = client.get(filtered_url)
        parsed_response = response.json()
        self.assertEqual(len(parsed_response), 0)

        filtered_url = '{}?timestamp_after={}'.format(
                reverse('test-suite-list'),
                (timestamp + timedelta(1)).isoformat()
                )

        response = client.get(filtered_url)
        parsed_response = response.json()
        self.assertEqual(len(parsed_response), 0)

        filtered_url = '{}?timestamp_after={}&timestamp_before={}'.format(
                reverse('test-suite-list'),
                (timestamp - timedelta(0, 3600)).isoformat(),
                (timestamp + timedelta(0, 3600)).isoformat()
                )

        response = client.get(filtered_url)
        parsed_response = response.json()

        self.assertTrue(len(parsed_response) > 1)
