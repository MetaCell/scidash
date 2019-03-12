import requests
import json
from django.conf import settings as s

from scidash.general.helpers import import_class

import pygeppetto_gateway as pg


def download_and_save_model(path, url):
    model_content = requests.get(url)

    with open(path, 'w') as f:
        f.write(model_content.text)


def check_capabilities(model_file_path, model_class_import_path):
    klass = import_class(model_class_import_path)

    try:
        failed = klass(model_file_path).failed_extra_capabilities
    except Exception:
        return False

    return len(failed) == 0


def get_model_capabilities(model_class_import_path):
    klass = import_class(model_class_import_path)

    doll = s.MODEL_DOLL

    return klass(doll).capabilities


def get_extra_capabilities(model_class_import_path):
    klass = import_class(model_class_import_path)

    doll = s.MODEL_DOLL

    return klass(doll).extra_capability_checks


def get_model_parameters(url):
    servlet_manager = pg.GeppettoServletManager()

    builder = pg.GeppettoProjectBuilder(
        nml_url=url,
        project_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/p.json",
        xmi_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/m.xmi",
        nml_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/nml_model.nml"
    )
    project_url = builder.build_project()

    servlet_manager.handle('load_project_from_url', project_url)

    wrong_message = True
    result = {}

    while wrong_message:
        result = json.loads(servlet_manager.read())
        print(result.get('type'))
        wrong_message = result.get(
            'type'
        ) != 'geppetto_model_loaded' and result.get('type') != 'generic_error'

    if result.get('type') == 'generic_error':
        result = json.loads(result.get('data'))
        result = json.loads(result.get('message'))

        raise Exception(result)

    return result
