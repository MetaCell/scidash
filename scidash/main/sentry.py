import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration


sentry_environment = os.environ.get("ENVIRONMENT", "Production")


def init():
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN', ""),
        environment=sentry_environment,
        integrations=[CeleryIntegration(),
                        DjangoIntegration(),
                        RedisIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
