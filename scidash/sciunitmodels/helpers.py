import json
import logging
import os
import time
import typing as t

import enforce
import requests
from django.conf import settings as s

import pygeppetto_gateway as pg
from scidash.general.helpers import import_class

db_logger = logging.getLogger('db')
enforce.config({'mode': 'covariant'})


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


def get_model_parameters(url: t.Union[str, dict], model_id: str) -> dict:
    servlet_manager = pg.GeppettoServletManager.get_instance()

    if isinstance(url, dict):
        extractor = pg.interpreters.helpers.NeuroMLDbExtractor(
            url, model_id, '/tmp/'
        )
        file_name = extractor.root_file
    else:
        file_name = os.path.basename(url)

    if isinstance(url, dict):
        interpreter_string = pg.interpreters.helpers.interpreter_detector(
            file_name
        )
    else:
        interpreter_string = pg.interpreters.helpers.interpreter_detector(url)

    interpreter_class = import_class(interpreter_string)
    timestamp = int(time.time())

    builder = pg.GeppettoProjectBuilder(
        model_file_url=url,
        interpreter=interpreter_class,
        project_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/{timestamp}/p.json",  # noqa: E501
        xmi_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/{timestamp}/m.xmi",  # noqa: E501
        model_file_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/{timestamp}/{file_name}"  # noqa: E501
    )
    project_url = builder.build_project()

    servlet_manager.handle('load_project_from_url', project_url)

    wrong_message = True
    result = {}

    while wrong_message:
        result = servlet_manager.read()
        db_logger.info(result)

        parsed_result = json.loads(result)

        wrong_message = parsed_result.get(
            'type'
        ) != 'geppetto_model_loaded' and parsed_result.get(
            'type'
        ) != 'generic_error'

    if parsed_result.get('type') == 'generic_error':
        parsed_result = json.loads(parsed_result.get('data'))
        parsed_result = json.loads(parsed_result.get('message'))

        raise Exception(parsed_result)

    return parsed_result
