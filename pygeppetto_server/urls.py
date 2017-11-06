from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^org.geppetto.frontend/geppetto/(?P<path>.*)',
        RedirectView.as_view(url='/static/org.geppetto.frontend/src/main/webapp/%(path)s')
        ),
]
