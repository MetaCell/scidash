import os
import json

from django.test import TestCase, Client
from django.urls import reverse

from sciunittests.serializers import ScoreSerializer

SAMPLE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),
        'json_sample.json')


class SciunitTestTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SciunitTestTestCase, cls).setUpClass()

        with open(SAMPLE_FILE) as f:
            score_serializer = ScoreSerializer(data=json.loads(f.read()))

        if score_serializer.is_valid():
            score_serializer.save()

    def test_if_scores_endpoint_works_correctly(self):
        client = Client()

        response = client.get(reverse('score-list'))

        parsed_response = response.json()

        print(parsed_response)
