import uuid

from src.modules.project.update_project.app.update_project_controller import UpdateProjectController
from src.modules.project.update_project.app.update_project_usecase import UpdateProjectUsecase
from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class MockHttpRequest:
    def __init__(self, data: dict):
        self.data = data


class TestUpdateProjectController:

    def setup_method(self):
        self.repo = ProjectRepositoryMock()
        self.usecase = UpdateProjectUsecase(self.repo)
        self.controller = UpdateProjectController(self.usecase)


    def test_update_project_success(self):

        project_id = str(self.repo.projects[0].id)

        data = {
            "project_id" : project_id,
            "title" : "Novo Título",
            "description" : "Nova descrição",
            "cell_image" : "novo.jpeg",
            "tech_frontend" : "Vue",
            "tech_backend" : "Node",
            "color" : "#123456"
        }

        request = MockHttpRequest(data = data)
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.OK.value
        assert response.body["project_id"] == project_id
        assert response.body["project_title"] == "Novo Título"
        assert response.body["project_description"] == "Nova descrição"
        assert response.body["project_cell_image"] == "novo.jpeg"
        assert response.body["project_tech_frontend"] == "Vue"
        assert response.body["project_tech_backend"] == "Node"


    def test_update_project_missing_project_id(self):
        data = {
            "title": "Novo Título" #passando informação aleatoria aq
        }

        request = MockHttpRequest(data = data)
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value


    def test_update_project_wrong_type(self):
        data = {
            "project_id": 123
        }

        request = MockHttpRequest(data = data)
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value


    def test_update_project_not_found(self):
        data = {
            "project_id": str(uuid.uuid4())
        }

        request = MockHttpRequest(data = data)
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.NOT_FOUND.value