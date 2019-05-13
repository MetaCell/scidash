import collections
import copy
import json
import os
import re

import quantities as pq
from django.conf import settings
from django.views import View
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from scidash.general import helpers as general_hlp
from scidash.general.backends import ScidashCacheBackend
from scidash.sciunitmodels import helpers as model_hlp
from scidash.sciunittests.models import ScoreClass, ScoreInstance
from scidash.sciunittests.serializers import ScoreInstanceSerializer


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, )
    permission_classes = (IsAuthenticated, )

    errors = []

    def put(self, request, filename):
        sciunit_serialized_score_file = request.data['file']

        parsed_data = \
            json.loads(sciunit_serialized_score_file.read().decode('utf-8'))
        instance = self.populate_data(parsed_data, request)

        if instance:
            return Response({'success': True, 'data': instance}, status=201)
        else:
            return Response(
                {
                    'success': False,
                    'errors': self.errors
                }, status=400
            )

    def populate_data(self, data, request):
        score_serializer = ScoreInstanceSerializer(
            data=data, context={'request': request}
        )

        if score_serializer.is_valid():
            score_serializer.save()
            return score_serializer.data
        else:
            self.errors = score_serializer.errors
            return False


class GeppettoHandlerView(View):

    OUTPUT_MAPPING_FILE = 'outputMapping.dat'
    RESULTS_FILE = 'results0.dat'
    TIME_VAR_REGEXP = '^time\(\w+\)$'

    def get_variable_from_header(self, header):
        if re.match(self.TIME_VAR_REGEXP, header):
            return 't'
        else:
            return header

    def calculate_score(self, simulation_result, score_instance):
        model_class = general_hlp.import_class(
            score_instance.model_instance.model_class.import_path
        )

        model_url = score_instance.model_instance.url
        model_name = os.path.basename(model_url)
        model_path = os.path.join(settings.DOWNLOADED_MODEL_DIR, model_name)

        model_hlp.download_and_save_model(model_path, model_url)

        model_instance = model_class(
            model_path,
            name=score_instance.model_instance.name,
            backend=ScidashCacheBackend.name
        )

        model_instance.set_memory_cache(simulation_result)

        test_class = general_hlp.import_class(
            score_instance.test_instance.test_class.import_path
        )

        observation = copy.deepcopy(score_instance.test_instance.observation)
        params = copy.deepcopy(score_instance.test_instance.params)

        try:
            destructured = json.loads(
                score_instance.test_instance.test_class.units
            )
        except json.JSONDecodeError:
            units = general_hlp.import_class(
                score_instance.test_instance.test_class.units
            )
        else:
            if destructured.get('name', False):
                base_unit = general_hlp.import_class(
                    destructured.get('base').get('quantity')
                )
                units = pq.UnitQuantity(
                    destructured.get('name'),
                    base_unit * destructured.get('base').get('coefficient'),
                    destructured.get('symbol')
                )
            else:
                units = destructured

        for key in observation:
            if not isinstance(units, dict):
                observation[key] = int(observation[key]
                                       ) * units if key != 'n' else int(
                                           observation[key]
                                       )
            else:
                observation[key] = int(observation[key]
                                       ) * units[key] if key != 'n' else int(
                                           observation[key]
                                       )

        params_units = score_instance.test_instance.test_class.params_units

        for key in params_units:
            params_units[key] = general_hlp.import_class(params_units[key])

        processed_params = {}

        for key in params:
            if params[key] is not None:
                processed_params[key] = float(params[key]) * params_units[key]

        test_instance = test_class(observation=observation, **processed_params)

        score = test_instance.judge(model_instance).json(
            add_props=True, string=False
        )

        self.update_score(score_instance, score)

        return score

    def update_score(self, score_instance, score_data):
        score_class = None

        score_class, created = ScoreClass.objects.get_or_create(
            url=score_data.get('_class').get('url'),
            class_name=score_data.get('_class').get('name')
        )

        score_instance.score_class = score_class
        score_instance.score = score_data.get('score')

        sort_key = score_data.get('norm_score') if not score_data.get(
            'sort_key', False
        ) else score_data.get('sort_key')

        if sort_key is None:
            score_instance.sort_key = 0
        else:
            score_instance.sort_key = sort_key

        prediction = score_data.get('prediction', None)

        if prediction is not None:
            if isinstance(prediction, dict):
                score_instance.prediction_dict = prediction
            else:
                score_instance.prediction_numeric = prediction

        score_instance.raw = score_data.get('raw', None)
        score_instance.status = ScoreInstance.CALCULATED
        score_instance.summary = score_data.get('summary', None)

        score_instance.save()

    def post(self, request):
        body = json.loads(request.body)
        results = json.loads(body.get('experiment_results', ''))
        score_pk = body.get('scoreID')

        try:
            score_instance = ScoreInstance.objects.get(pk=score_pk)
        except ScoreInstance.DoesNotExists:
            return Response(
                {
                    'success': False,
                    'message': 'Score not found'
                }, 404
            )

        output_mapping = list(
            filter(
                lambda x: os.path.basename(x) == self.OUTPUT_MAPPING_FILE,
                results
            )
        ).pop().replace('file:', '')

        results_file = list(
            filter(
                lambda x: os.path.basename(x) == self.RESULTS_FILE, results
            )
        ).pop().replace('file:', '')

        simulation_result = None

        with open(output_mapping, 'r') as f:
            splat = f.read().split('\n')

            simulation_result = collections.OrderedDict(
                {
                    self.get_variable_from_header(header): None
                    for header in splat[1].split(' ')
                }
            )

        with open(results_file, 'r') as f:
            values = [[] for i in range(len(simulation_result.keys()))]

            for line in f:
                splat = line.split('\t')

                for i, value in enumerate(values):
                    values[i].append(splat[i])

        for i, (key, value) in enumerate(simulation_result.items()):
            simulation_result[key] = list(map(lambda x: float(x), values[i]))

        score = self.calculate_score(simulation_result, score_instance)

        return Response(data=score)
