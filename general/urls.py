from django.conf.urls import url
from general.views import FileUploadView

urlpatterns = [
        url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
        ]
