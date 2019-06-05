import json
import logging
import os
import time
import re
import typing as t

import requests
from django.conf import settings as s
import enforce

import pygeppetto_gateway as pg
from scidash.general.helpers import import_class

db_logger = logging.getLogger('db')
enforce.config({
    'mode': 'covariant'
})


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


def get_model_parameters(url: str) -> dict:
    servlet_manager = pg.GeppettoServletManager()
    file_name = os.path.basename(url)

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

    servlet_manager.close()

    return parsed_result


class URLProcessorException(Exception):
    pass


@enforce.runtime_validation
class URLProcessor():

    GITHUB_BLOB = 'github'
    GITHUB_RAW = 'githubusercontent'
    NEUROML_DB = 'neuroml-db'

    def __init__(self, url: str) -> None:
        self.url = url

        self.type = self.detect_type()

        db_logger.info(f'URL Processor got {self.type} url')

    def detect_type(self) -> str:
        if self.GITHUB_RAW not in self.url and self.GITHUB_BLOB in self.url:
            return self.GITHUB_BLOB

        if self.NEUROML_DB in self.url:
            return self.NEUROML_DB

        return self.GITHUB_RAW

    def get_file_url(self) -> t.Union[str, dict]:
        if self.type == self.GITHUB_RAW:
            return self.url

        if self.type == self.GITHUB_BLOB:
            return self.convert_github()

        if self.type == self.NEUROML_DB:
            return self.convert_neuromldb()

    def convert_github(self) -> str:
        result = self.url

        result = result.replace("blob/", "")
        result = result.replace("github.com", "raw.githubusercontent.com")

        return result

    def convert_neuromldb(self) -> dict:
        regexp = 'model_info?model_id=([\w])$'

        result = re.search(regexp, self.url)

        if result is not None:
            model_id = result.group(1)
        else:
            raise URLProcessorException(
                f'Can\'t found model id for url {self.url}'
            )

        return {
            'api': f'https://neuroml-db.org/api/model?id={model_id}',
            'zip': f'https://neuroml-db.org/GetModelZip?modelID={model_id}&version=NeuroML'
        }
