import os
from random import getrandbits as grb

import quantities as pq
from django.conf import settings as s
from rest_framework.response import Response
from rest_framework.views import APIView

from scidash.general.helpers import import_class
from scidash.sciunitmodels.helpers import download_and_save_model
from scidash.sciunitmodels.models import ModelInstance
from scidash.sciunittests.models import ScoreInstance, TestInstance
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

    def post(self, request):
        tests = request.data.get('tests')
        models = request.data.get('models')

        observation = {'mean': 1 * pq.ms, 'std': 1 * pq.ms}

        test_models = [
            test for test in TestInstance.objects.filter(id__in=tests)
        ]

        model_models = [
            model for model in ModelInstance.objects.filter(id__in=models)
        ]

        test_instances = [
            import_class(test.test_class.import_path
                         )(observation, name=f'{test.name}#{test.pk}')
            for test in test_models
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
        matrix = request.data
        result = []

        for model_pk in matrix.keys():
            try:
                model_instance = ModelInstance.objects.get(pk=model_pk)
            except ModelInstance.DoesNotExist as e:
                return Response({'success': False, 'message': e})

            test_ids = [test_pk for test_pk in matrix.get(model_pk)]

            test_instances = TestInstance.objects.filter(pk__in=test_ids)

            scores = []

            for test in test_instances:
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
