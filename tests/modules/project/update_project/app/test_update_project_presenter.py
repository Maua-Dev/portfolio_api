import json
import os

os.environ["STAGE"] = "TEST"
from src.modules.project.update_project.app import update_project_presenter as presenter_module
from src.modules.project.update_project.app.update_project_presenter import update_project_presenter



def build_event(project_id: str = None, title: str = None, description: str = None, cell_image: str = None,
                tech_frontend: str = None, tech_backend: str = None, color: str = None) -> dict:
    return {
        'queryStringParameters': {
            'project_id': project_id,
            'title': title,
            'description': description,
            'cell_image': cell_image,
            'tech_frontend': tech_frontend,
            'tech_backend': tech_backend,
            'color': color
        }
}

class TestUpdateProjectPresenter:

    def test_update_project_presenter_success(self):
        
        project_id = str(presenter_module.repo.projects[0].id)
        event = build_event(
            project_id = project_id,
            title = "Novo Titulo",
            description = "Nova descrição",
            cell_image = "novo.jpeg",
            tech_frontend = "Vue",
            tech_backend = "Node",
            color = "#123456"
        )

        response = update_project_presenter(event)
        body = json.loads(response['body'])

        assert response["statusCode"] == 200
        assert body["project_id"] == project_id
        assert body["project_title"] == "Novo Titulo"
        assert body["project_description"] == "Nova descrição"
        assert body["project_cell_image"] == "novo.jpeg"
        assert body["project_tech_frontend"] == "Vue"
        assert body["project_tech_backend"] == "Node"
        assert body["project_color"] == "#123456"