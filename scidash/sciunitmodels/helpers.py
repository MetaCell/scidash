import json
import logging
import os

import requests
from django.conf import settings as s

import pygeppetto_gateway as pg
from scidash.general.helpers import import_class

db_logger = logging.getLogger('db')


def download_and_save_model(path, url):
    model_content = requests.get(url)

    pg.helpers.process_includes(url)

    with open(path, 'w') as f:
        f.write(model_content.text)


def check_capabilities(model_file_path, model_class_import_path):
    klass = import_class(model_class_import_path)

    try:
        failed = klass(model_file_path).failed_extra_capabilities
    except Exception as e:
        db_logger.exception(e)
        return False

    return len(failed) == 0


def get_model_capabilities(model_class_import_path):
    klass = import_class(model_class_import_path)

    return klass.get_capabilities()


def get_extra_capabilities(model_class_import_path):
    klass = import_class(model_class_import_path)

    if klass.extra_capability_checks is not None:
        return klass.extra_capability_checks
    else:
        return {}


def get_model_parameters(url):
    servlet_manager = pg.GeppettoServletManager()
    file_name = os.path.basename(url)

    builder = pg.GeppettoProjectBuilder(
        model_url=url,
        project_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/p.json",
        xmi_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/m.xmi",
        nml_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/{file_name}"
    )
    project_url = builder.build_project()

    servlet_manager.handle('load_project_from_url', project_url)

    wrong_message = True
    result = {}

    while wrong_message:
        result = json.loads(servlet_manager.read())
        wrong_message = result.get(
            'type'
        ) != 'geppetto_model_loaded' and result.get('type') != 'generic_error'

    if result.get('type') == 'generic_error':
        result = json.loads(result.get('data'))
        result = json.loads(result.get('message'))

        raise Exception(result)

    return result
