import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from scidash.sciunittests.serializers import ScoreInstanceSerializer


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    errors = []

    def put(self, request, filename):
        sciunit_serialized_score_file = request.data['file']

        parsed_data = \
        json.loads(sciunit_serialized_score_file.read().decode('utf-8'))
        instance = self.populate_data(parsed_data, request)

        if instance:
            return Response({'success': True, 'data': instance}, status=201)
        else:
            return Response({'success': False, 'errors': self.errors},
                            status=400)

    def populate_data(self, data, request):
        score_serializer = ScoreInstanceSerializer(data=data,
                context={'request': request})

        if score_serializer.is_valid():
            score_serializer.save()
            return score_serializer.data
        else:
            self.errors = score_serializer.errors
            return False
