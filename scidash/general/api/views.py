import quantities as pq
from sciunit import TestSuite
from django.conf import settings as s
from rest_framework.views import APIView
from rest_framework.response import Response
from scidash.general.helpers import import_class
from scidash.sciunitmodels.models import ModelInstance
from scidash.sciunittests.models import TestInstance
import json


class CompatibilityMatrixView(APIView):
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
            import_class(model.model_class.import_path
                         )(s.MODEL_DOLL, name=f'{model.name}#{model.pk}')
            for model in model_models
        ]

        suite = TestSuite(test_instances)
        result = suite.check(model_instances)

        return Response(
            {
                'compatibility': result.to_csv(
                    sep='|', line_terminator="/"
                )
            }
        )
