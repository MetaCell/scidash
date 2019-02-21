import requests

from scidash.general.helpers import import_class


def download_and_save_model(path, url):
    model_content = requests.get(url)

    with open(path, 'w') as f:
        f.write(model_content)


def check_capabilities(model_file_path, model_class_import_path):
    klass = import_class(model_class_import_path)

    return klass.failed_extra_capabilities


def get_model_capabilities(model_class_import_path):
    klass = import_class(model_class_import_path)

    return klass.capabilities


def get_extra_capabilities(model_class_import_path):
    klass = import_class(model_class_import_path)

    return klass.extra
