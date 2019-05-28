import json
import os
import logging

from celery import shared_task
from django.conf import settings as s

import pygeppetto_gateway as pg
from websocket import WebSocketTimeoutException
from pygeppetto_server.messages import Servlet as S
from pygeppetto_server.messages import ServletResponse as SR
from scidash.sciunittests.models import ScoreInstance as Score
from scidash.general.helpers import import_class
from pygeppetto_gateway.interpreters.helpers import interpreter_detector

db_logger = logging.getLogger('db')


def get_project_id(raw_data):
    data = json.loads(raw_data)
    project_data = json.loads(data.get('project_loaded'))
    db_logger.info(project_data)

    return project_data.get('project').get('id')


def get_error(raw_data):
    return raw_data


def send_score_to_geppetto(score):
    db_logger.info(f'Processing score with ID {score.pk}')
    model_name = os.path.basename(score.model_instance.url)
    interpreter = import_class(interpreter_detector(score.model_instance.url))

    project_builder = pg.GeppettoProjectBuilder(
        score=score,
        interpreter=interpreter,
        project_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/{score.owner}/{score.pk}/project.json",  # noqa:E501
        xmi_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/{score.owner}/{score.pk}/model.xmi",  # noqa:E501
        model_file_location=f"{s.PYGEPPETTO_BUILDER_PROJECT_BASE_URL}/{score.owner}/{score.pk}/{model_name}",  # noqa:E501
    )

    project_url = project_builder.build_project()

    servlet_manager = pg.GeppettoServletManager()
    servlet_manager.handle(S.LOAD_PROJECT_FROM_URL, project_url)

    project_loaded = False
    model_loaded = False

    project_id = None

    while not project_loaded and not model_loaded:
        try:
            response = json.loads(servlet_manager.read())
        except Exception as e:
            return e

        response_type = response.get('type')

        db_logger.info(response_type)

        if response_type == SR.GENERIC_ERROR or response_type == SR.ERROR_LOADING_PROJECT:  # noqa: E501
            error = get_error(response.get('data'))
            db_logger.error(error)

            return error

        project_loaded = response_type == SR.PROJECT_LOADED
        model_loaded = response_type == SR.GEPPETTO_MODEL_LOADED

        if project_loaded:
            project_id = get_project_id(response.get('data'))
            db_logger.info(project_id)

    if project_id is None:
        return "Project not found"

    score.status = Score.LOCKED
    score.save()

    servlet_manager.handle(
        S.RUN_EXPERIMENT,
        json.dumps({
            'projectId': project_id,
            'experimentId': 1
        })
    )

    finished = False
    experiment_loaded = False

    while not finished:
        try:
            response = json.loads(servlet_manager.read())
        except WebSocketTimeoutException:
            db_logger.info('Successfully started experiment')
            return True
        except Exception as e:
            db_logger.error(e)
            score.error = e
            score.status = score.FAILED
            score.save()

        response_type = response.get('type')

        db_logger.info(response_type)

        if response_type == SR.ERROR_RUNNING_EXPERIMENT:
            error = get_error(response.get('data'))
            db_logger.error(error)
            score.error = error
            score.status = score.FAILED
            score.save()

            return error

        experiment_loaded = response_type == SR.EXPERIMENT_LOADED

        if experiment_loaded:
            db_logger.info(f'Score with ID {score.pk} successfully sent')


@shared_task
def run_experiment():
    scores = Score.objects.filter(status=Score.SCHEDULED)

    for score in scores:
        send_score_to_geppetto(score)
