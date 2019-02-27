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
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_cache.registry import cache_registry
from rest_framework_jwt.views import obtain_jwt_token

from scidash.account.api.views import CheckIsLoggedView, UserViewSet
from scidash.account.views import signup
from scidash.sciunitmodels.api import views as models_views
from scidash.sciunittests.api import views as tests_views
from scidash.sciunittests.views import DateRangeView

cache_registry.autodiscover()

router = DefaultRouter()
# Models Views
router.register(
    r'capabilities', models_views.CapabilityViewSet, base_name='capability'
)
router.register(
    r'model-classes', models_views.ModelClassViewSet, base_name='model-class'
)
router.register(
    r'model-instances',
    models_views.ModelInstanceViewSet,
    base_name='model-instance'
)

# Tests Views
router.register(r'scores', tests_views.ScoreViewSet, base_name='score')
router.register(
    r'test-classes', tests_views.TestClassViewSet, base_name='test-class'
)
router.register(
    r'test-instances',
    tests_views.TestInstanceViewSet,
    base_name='test-instance'
)
router.register(
    r'test-suites', tests_views.TestSuiteViewSet, base_name='test-suite'
)
router.register(
    r'score-classes', tests_views.ScoreClassViewSet, base_name='score-class'
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/login/$', obtain_jwt_token),
    url(r'^data/', include('scidash.general.urls')),
    url(r'^api/date-range/$', DateRangeView.as_view(), name='date-range-view'),
    url(r'^api/', include(router.urls)),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(
        r'^auth/password-reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password-reset-done.html'
        ),
        name='password-reset-done'
    ),
    url(
        r'^auth/password-reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password-reset.html',
            success_url='/auth/password-reset/done'
        ),
        name='password-reset'
    ),
    url(r'^auth/sign-up/$', signup, name='sign-up'),
    url(
        r'^api/users/me/$',
        UserViewSet.as_view({'get': 'retrieve'}),
        kwargs={'pk': 'me'},
        name='user-info'
    ),
    url(
        r'^api/users/is-logged/$',
        CheckIsLoggedView.as_view(),
        name='is-logged'
    ),
    url(r'^', include('pygeppetto_server.urls')),
]
