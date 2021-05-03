import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration

global sio_app
global sio_sys

sentry_environment = os.environ.get("ENVIRONMENT", "Production")


def _capture(msg, app=False, extra_context=None, f=sentry_sdk.capture_message):
    if extra_context is None:
        extra_context = {}
    with sentry_sdk.push_scope() as scope:
        scope.set_extra('type', 'app' if app else '')
        [scope.set_extra(key, value) for key, value in extra_context.items()]
        sentry_id = f(msg)
    return sentry_id


def capture_message(message="", app=False, extra_context=None):
    return _capture(msg=message, app=app, extra_context=extra_context)


def capture_exception(e, app=False, extra_context=None):
    return _capture(msg=e, app=app, extra_context=extra_context,
                    f=sentry_sdk.capture_exception)


def send_event(event):
    if 'extra' in event and \
       'type' in event['extra'] and \
       'app' in event['extra']['type'].lower():
        sio_app.capture_event(event)
    else:
        sio_sys.capture_event(event)


def init():
    global sio_app
    global sio_sys
    if sentry_sdk.Hub.current.client is None:
        sentry_dsn_sys = os.environ.get('SENTRY_SYS_DSN',
                                        os.environ.get('SENTRY_DSN', ""))
        sentry_dsn_app = os.environ.get('SENTRY_APP_DSN',
                                        sentry_dsn_sys)
        sio_app = sentry_sdk.client.Client(sentry_dsn_app)
        sio_sys = sentry_sdk.client.Client(sentry_dsn_sys)
        sentry_sdk.init(
            transport=send_event,
            environment=sentry_environment,
            integrations=[CeleryIntegration(),
                          DjangoIntegration(),
                          RedisIntegration()],

            # If you wish to associate users to errors (assuming you are using
            # django.contrib.auth) you may enable sending PII data.
            send_default_pii=True
        )
