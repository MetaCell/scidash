from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response


class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        sciunit_serialized_score = request.data['file']
        # ...
        #
        # ...
        return Response({'success': True}, status=201)
