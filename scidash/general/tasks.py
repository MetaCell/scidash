from celery import shared_task, utils
import json
from scidash.sciunittests.models import ScoreInstance as Score
import pygeppetto_gateway as pg
from pygeppetto_server.messages import Servlet as S, ServletResponse as SR

logger = utils.log.get_task_logger(__name__)


def get_project_id(raw_data):
    data = json.loads(raw_data)
    project_data = json.loads(data.get('project_loaded'))
    logger.info(project_data)

    return project_data.get('project').get('id')


def get_error(raw_data):
    return raw_data


@shared_task
def run_experiment():
    scores = Score.objects.filter(status=Score.SCHEDULED)

    for score in scores:
        logger.info(f'Processing score with ID {score.pk}')

        model_instance = score.model_instance
        project_builder = pg.GeppettoProjectBuilder(model_instance.url)

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

            logger.info(response_type)

            if response_type == 'generic_error':
                return get_error(response.get('data'))

            project_loaded = response_type == SR.PROJECT_LOADED
            model_loaded = response_type == SR.GEPPETTO_MODEL_LOADED

            if project_loaded:
                project_id = get_project_id(response.get('data'))
                logger.info(project_id)

        if project_id is None:
            return "Project not found"

        score.status = Score.LOCKED
        score.save()

        servlet_manager.handle(S.RUN_EXPERIMENT, json.dumps({
            'projectId': project_id,
            'experimentId': 1
        }))
