import json
from src.modules.project.get_all_projects.app.get_all_projects_presenter import lambda_handler

class Test_GetAllProjectsPresenter:
    def test_get_all_projects_presenter(self):
        event = {}
        response = lambda_handler(event, None)
        assert response["statusCode"] == 200
        assert json.loads(response["body"])["message"] == "projects were retreived successfully"
        assert len(json.loads(response["body"])["projects"]) == 3
