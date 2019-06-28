import json
import os

from django.core.management.base import BaseCommand

from scidash.sciunittests.models import TestClass
from scidash.sciunitmodels.models import ModelClass


class Command(BaseCommand):
    help = 'Population of model and test classes'

    def handle(self, *args, **options):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(current_dir, 'test_classes.json')) as f:
            classes = f.read()

        classes = json.loads(classes)

        for model in classes:
            obj, created = TestClass.objects.get_or_create(
                **model
            )
            obj.clean_fields()
            obj.save()

        with open(os.path.join(current_dir, 'model_classes.json')) as f:
            classes = f.read()

        classes = json.loads(classes)

        for model in classes:
            obj, created = ModelClass.objects.get_or_create(
                **model
            )
