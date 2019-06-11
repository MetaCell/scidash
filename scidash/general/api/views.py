import json
import os
from random import getrandbits as grb

import numpy as np
import quantities as pq
from django.conf import settings as s
from rest_framework.response import Response
from rest_framework.views import APIView

from scidash.general.helpers import import_class
from scidash.sciunitmodels.helpers import download_and_save_model
from scidash.sciunitmodels.models import ModelInstance
from scidash.sciunittests.models import ScoreInstance, TestInstance
from scidash.sciunittests.models import TestSuite as TestSuiteModel
from scidash.sciunittests.serializers import ScoreInstanceSerializer
from sciunit import TestSuite


class CompatibilityMatrixView(APIView):
    def _create_model_instance(self, model_object):
        models_file_path = s.DOWNLOADED_MODEL_DIR
        file_name = os.path.basename(model_object.url)

        path = f"{models_file_path}/{file_name}"
        download_and_save_model(path, model_object.url)

        return import_class(
            model_object.model_class.import_path
        )(path, name=f'{model_object.name}#{model_object.pk}')

    # FIXME: replace with helper
    def from_destructured(self, unit_dict):
        unit = pq.UnitQuantity(
            unit_dict.get('name'),
            import_class(unit_dict.get('base').get('quantity')) *
            unit_dict.get('base').get('coefficient'), unit_dict.get('symbol')
        )

        return unit

    def get_observation(self, units, observation) -> dict:

        try:
            imported_units = json.loads(units)

            if imported_units.get('name', False):
                imported_units = self.from_destructured(imported_units)
        except Exception:
            imported_units = import_class(imported_units)

        if not isinstance(imported_units, dict):
            for key in observation.keys():
                if key != 'n':
                    observation[key] = float(observation[key]) * imported_units
                else:
                    observation[key] = int(observation[key])
        else:
            imported_units = {
                param: import_class(unit)
                for param, unit in imported_units.items()
            }
            for key in observation.keys():
                if key != 'n':
                    observation[key] = self.process_obs(observation[key]
                                                        ) * imported_units[key]
                else:
                    observation[key] = int(observation[key])

        return observation

    def process_obs(self, obs):
        try:
            observation = float(obs)
        except ValueError:
            observation = np.array(json.loads(obs))

        return observation

    def post(self, request):
        tests = request.data.get('tests')
        models = request.data.get('models')

        test_models = [
            test for test in TestInstance.objects.filter(id__in=tests)
        ]

        model_models = [
            model for model in ModelInstance.objects.filter(id__in=models)
        ]

        test_instances = [
            import_class(test.test_class.import_path)(
                self.get_observation(test.test_class.units, test.observation),
                name=f'{test.name}#{test.pk}'
            ) for test in test_models
        ]

        model_instances = [
            self._create_model_instance(model) for model in model_models
        ]

        suite = TestSuite(test_instances)
        result = suite.check(model_instances)

        return Response(
            {'compatibility': result.to_csv(sep='|', line_terminator=";")}
        )


class CreateScoresFromMatrixView(APIView):
    def post(self, request):
        matrix = request.data.get('matrix')
        suite_name = request.data.get('suiteName')
        save_suite = suite_name != ''
        result = []

        if save_suite:
            test_suite = TestSuiteModel.objects.create(
                owner=request.user, name=suite_name, hash=f"{grb(128)}"
            )

        for model_pk in matrix.keys():
            try:
                model_instance = ModelInstance.objects.get(pk=model_pk)
            except ModelInstance.DoesNotExist as e:
                return Response({'success': False, 'message': e})

            test_ids = [test_pk for test_pk in matrix.get(model_pk)]

            test_instances = TestInstance.objects.filter(pk__in=test_ids)

            scores = []

            for test in test_instances:
                if save_suite:
                    test.test_suites.add(test_suite)

                scores.append(
                    ScoreInstance(
                        model_instance=model_instance,
                        test_instance=test,
                        hash_id=f"{grb(128)}_{grb(22)}",
                        status=ScoreInstance.SCHEDULED,
                        owner=request.user
                    )
                )

                result.append(
                    list(ScoreInstanceSerializer(scores, many=True).data)
                )

            ScoreInstance.objects.bulk_create(scores)

        return Response(result)
