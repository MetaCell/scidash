import requests
from django.conf import settings

from scidash.general.helpers import import_class


def download_and_save_model(path, url):
    model_content = requests.get(url)

    with open(path, 'w') as f:
        f.write(model_content.text)


def check_capabilities(model_file_path, model_class_import_path):
    klass = import_class(model_class_import_path)

    failed = klass(model_file_path).failed_extra_capabilities

    return len(failed) == 0


def get_model_capabilities(model_class_import_path):
    klass = import_class(model_class_import_path)

    doll = settings.MODEL_DOLL

    return klass(doll).capabilities


def get_extra_capabilities(model_class_import_path):
    klass = import_class(model_class_import_path)

    doll = settings.MODEL_DOLL

    return klass(doll).extra_capability_checks
