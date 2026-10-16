from src.modules.project.get_all_projects.app.get_all_projects_controller import GetAllProjectsController
from src.modules.project.get_all_projects.app.get_all_projects_usecase import GetAllProjectsUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock

class Test_GetAllProjectsController:
    def test_get_all_projects_controller(self):
        repo = ProjectRepositoryMock()
        usecase = GetAllProjectsUsecase(repo=repo)
        controller = GetAllProjectsController(usecase=usecase)
        
        request = HttpRequest()
        response = controller(request=request)
        
        assert response.status_code == 200
        assert response.body['message'] == "projects were retreived successfully"
        assert len(response.body['projects']) == 3
