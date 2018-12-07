"""pygeppetto_template URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from scidash.sciunitmodels.api import views as models_views
from scidash.sciunittests.api import views as tests_views
from scidash.sciunittests.views import DateRangeView
from scidash.account.views import signup

from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_cache.registry import cache_registry

cache_registry.autodiscover()

router = DefaultRouter()
# Models Views
router.register(r'capabilities', models_views.CapabilityViewSet,
        base_name='capability')
router.register(r'model-classes', models_views.ModelClassViewSet,
        base_name='model-class')
router.register(r'model-instances', models_views.ModelInstanceViewSet,
        base_name='model-instance')

# Tests Views
router.register(r'scores', tests_views.ScoreViewSet,
        base_name='score')
router.register(r'test-classes', tests_views.TestClassViewSet,
        base_name='test-class')
router.register(r'test-instances', tests_views.TestInstanceViewSet,
        base_name='test-instance')
router.register(r'test-suites', tests_views.TestSuiteViewSet,
        base_name='test-suite')
router.register(r'score-classes', tests_views.ScoreClassViewSet,
        base_name='score-class')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/login/', obtain_jwt_token),
    url(r'^', include('pygeppetto_server.urls'), name='home'),
    url(r'^data/', include('scidash.general.urls')),
    url(r'^api/date-range', DateRangeView.as_view(), name='date-range-view'),
    url(r'^api/', include(router.urls)),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^auth/sign-up/', signup, name='signup')
]
