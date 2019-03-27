from django.conf.urls import url

from scidash.general.views import FileUploadView, GeppettoHandlerView

urlpatterns = [
    url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
    url(r'^experiment-result/handle/$', GeppettoHandlerView.as_view())
]
