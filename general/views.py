import json

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from sciunittests.serializers import ScoreSerializer


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (AllowAny,)

    errors = []

    def put(self, request, filename):
        sciunit_serialized_score_file = request.data['file']

        parsed_data = json.loads(sciunit_serialized_score_file.read())
        instance = self.populate_data(parsed_data)

        if instance:
            return Response({'success': True, 'data': instance}, status=201)
        else:
            return Response({'success': False, 'errors': self.errors},
                            status=400)

    def populate_data(self, data):
        score_serializer = ScoreSerializer(data=data)

        if score_serializer.is_valid():
            score_serializer.save()
            return score_serializer.data
        else:
            self.errors = score_serializer.errors
            return False
