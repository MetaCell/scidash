from django.http import Http404
from rest_framework import response, views, viewsets

from scidash.account.serializers import ScidashUserSerializer
from scidash.general.models import ScidashUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = ScidashUser.objects.all()
    serializer_class = ScidashUserSerializer

    def get_object(self):

        if self.kwargs.get('pk', None) == 'me':
            if self.request.user.is_authenticated():
                self.kwargs['pk'] = self.request.user.pk
            else:
                raise Http404

        return super(UserViewSet, self).get_object()


class CheckIsLoggedView(views.APIView):
    def get(self, request, format=None):

        return response.Response(
            {
                'is_logged': self.request.user.is_authenticated()
            }
        )
