#!/usr/bin/env python
import os
import sys
import sentry_sdk

sentry_sdk.init("https://ccf48f7877bc4fb5a4cca74bdd193feb@sentry.io/1955654")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scidash.main.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
