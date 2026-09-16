import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.get_project.app import get_project_presenter as presenter_module
from src.modules.get_project.app.get_project_presenter import get_project_presenter


def build_event(project_id: str = None) -> dict:
    return {
        'queryStringParameters': {'project_id': project_id} if project_id else None
    }


class TestGetProjectPresenter:

    def test_get_project_presenter_success(self):
        project_id = str(presenter_module.repo.projects[0].id)
        event = build_event(project_id)

        response = get_project_presenter(event)
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert body['project_id'] == project_id
        assert body['project_title'] == 'Projeto Teste 1'
        assert body['project_description'] == 'Descrição projeto teste 1'
        assert body['project_tech_frontend'] == 'React'
        assert body['project_tech_backend'] == 'Python'
        assert body['project_color'] == 'white'

    def test_get_project_presenter_not_found(self):
        event = build_event(project_id='11111111-1111-1111-1111-111111111111')

        response = get_project_presenter(event)

        assert response['statusCode'] == 404

    def test_get_project_presenter_missing_id(self):
        event = build_event()

        response = get_project_presenter(event)

        assert response['statusCode'] == 400