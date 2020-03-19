"""
Django settings for scidash project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import datetime
import os

import dotenv
from django.urls import reverse

from .sentry import init as sentry_init

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

dotenv.read_dotenv(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'
    )
)

# SECURITY WARNING: don't run with debug turned on in production!
# Se via OS env, defaults to False
DEBUG = TEMPLATE_DEBUG = os.environ.get('DEVELOPMENT', '0') == '1'

if DEBUG:
    sentry_init()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4*0@ca#ocm*(1=12m(bfb2p8e$sk-%i4xlj=%$wkj3*&gs!%sr'

ALLOWED_HOSTS = [
    "*"
]

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]

THIRD_PARTY_APPS = [
    'pygeppetto_server',
    'channels',
    'rest_framework',
    'django_extensions',
    'django_filters',
    'rest_framework_cache',
    'material',
    'django_celery_beat',
    'django_celery_results',
    'django_db_logger'
]

SCIDASH_APPS = [
    'scidash.sciunitmodels',
    'scidash.sciunittests',
    'scidash.general',
    'scidash.account',
    'scidash.logviewer'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + SCIDASH_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'scidash.account.auth.CsrfExemptSessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

ROOT_URLCONF = 'scidash.main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, os.environ.get('STATIC_DIR'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'scidash.main.routing.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = os.environ.get('STATIC_URL')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, os.environ.get('STATIC_DIR'))
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['db_log'],
            'level': 'ERROR',
            'propagate': False,
        },
        'db': {
            'handlers': ['db_log'],
            'level': 'DEBUG'
        }
    }
}

AUTH_USER_MODEL = 'general.ScidashUser'

REST_FRAMEWORK_CACHE = {
    'DEFAULT_CACHE_TIMEOUT': 86400,  # Default is 1 day
}

PYGEPPETTO_SOCKET_URL = 'org.geppetto.frontend/GeppettoServlet'
PYGEPPETTO_BUILDER_PROJECT_BASE_URL = os.path.join(os.path.join(
    BASE_DIR, os.environ.get('STATIC_DIR')
), 'projects')

GEPPETTO_SERVLET_URL = os.environ.get(
    'GEPPETTO_SERVLET_URL',
    'ws://scidash-virgo:8080/org.geppetto.frontend/GeppettoServlet'
)
GEPPETTO_BASE_URL = os.environ.get(
    'GEPPETTO_BASE_URL',
    'http://scidash-virgo:8080/org.geppetto.frontend/geppetto'
)

BASE_PROJECT_FILES_HOST = os.environ.get(
    'BASE_PROJECT_FILES_HOST',
    'http://scidash:8000/static/projects/'
)

ACCEPTABLE_SCORE_INSTANCES_AMOUNT = 50

LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'user here'
EMAIL_HOST_PASSWORD = 'password here'
EMAIL_USE_SSL = True

POPULATE_USERS = True

DOWNLOADED_MODEL_DIR = os.path.join(
    BASE_DIR, os.environ.get('STATIC_DIR'), 'models'
)

CELERY_RESULT_BACKEND = 'django-db'

NO_IMPORT_TAG = 'unschedulable'

# SCIDASH
# DEMO user id used to clone initial models and tests from
SCIDASH_DEMO_USER_ID = None
