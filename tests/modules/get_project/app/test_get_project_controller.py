import uuid

from src.modules.get_project.app.get_project_controller import GetProjectController
from src.modules.get_project.app.get_project_usecase import GetProjectUsecase
from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock

class MockHttpRequest:
    def __init__(self, data: dict):
        self.data = data


class TestGetProjectController:

    def setup_method(self):
        self.repo = ProjectRepositoryMock()
        self.usecase = GetProjectUsecase(self.repo)
        self.controller = GetProjectController(self.usecase)

    def test_get_project_success(self):
        project_id = str(self.repo.projects[0].id)
        request = MockHttpRequest(data={'project_id': project_id})

        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.OK.value
        assert response.body['project_id'] == project_id
        assert response.body['project_title'] == 'Projeto Teste 1'
        assert response.body['project_description'] == 'Descrição projeto teste 1'
        assert response.body['project_tech_frontend'] == 'React'
        assert response.body['project_tech_backend'] == 'Python'
        assert response.body['project_color'] == 'white'

    def test_get_project_missing_project_id(self):
        request = MockHttpRequest(data={})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_get_project_wrong_type(self):
        request = MockHttpRequest(data={'project_id': 123})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_get_project_invalid_uuid(self):
        request = MockHttpRequest(data={'project_id': 'not-a-uuid'})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_get_project_not_found(self):
        request = MockHttpRequest(data={'project_id': str(uuid.uuid4())})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.NOT_FOUND.value