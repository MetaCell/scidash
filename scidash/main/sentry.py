import os
import sentry_sdk

from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration


def init():
    # sentry_sdk.init(
    #     dsn=settings.SENTRY_DSN,
    #     environment=settings.SENTRY_ENV,
    #     integrations=[CeleryIntegration(),
    #                     DjangoIntegration(),
    #                     RedisIntegration()],

    #     # Set traces_sample_rate to 1.0 to capture 100%
    #     # of transactions for performance monitoring.
    #     # We recommend adjusting this value in production.
    #     traces_sample_rate=1.0,

    #     # If you wish to associate users to errors (assuming you are using
    #     # django.contrib.auth) you may enable sending PII data.
    #     # send_default_pii=True
    # )
    pass
