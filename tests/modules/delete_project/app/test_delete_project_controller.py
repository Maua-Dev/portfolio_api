from src.modules.delete_project.app.delete_project_controller import DeleteProjectController
from src.modules.delete_project.app.delete_project_usecase import DeleteProjectUsecase
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class TestDeleteProjectController:
    def test_delete_project_controller(self):
        project_repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteProjectUsecase(project_repo, user_repo)
        controller = DeleteProjectController(usecase)
        
        project_id = str(project_repo.projects[0].id)
        admin_user_id = str(user_repo.users[0].id)
        
        request = HttpRequest(body={
            "project_id": project_id,
            "user_from_authorizer": {"user_id": admin_user_id}
        })
        
        response = controller(request)
        
        assert response.status_code == 200
        assert response.body["message"] == "the project was deleted successfully"

    def test_delete_project_controller_missing_project_id(self):
        project_repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteProjectUsecase(project_repo, user_repo)
        controller = DeleteProjectController(usecase)
        
        admin_user_id = str(user_repo.users[0].id)
        
        request = HttpRequest(body={
            "user_from_authorizer": {"user_id": admin_user_id}
        })
        
        response = controller(request)
        
        assert response.status_code == 400
        assert response.body == "Field project_id is missing"

    def test_delete_project_controller_missing_user_from_authorizer(self):
        project_repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteProjectUsecase(project_repo, user_repo)
        controller = DeleteProjectController(usecase)
        
        project_id = str(project_repo.projects[0].id)
        
        request = HttpRequest(body={
            "project_id": project_id
        })
        
        response = controller(request)
        
        assert response.status_code == 400
        assert response.body == "Field user_from_authorizer is missing"

    def test_delete_project_controller_wrong_type_project_id(self):
        project_repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteProjectUsecase(project_repo, user_repo)
        controller = DeleteProjectController(usecase)
        
        admin_user_id = str(user_repo.users[0].id)
        
        request = HttpRequest(body={
            "project_id": 123,
            "user_from_authorizer": {"user_id": admin_user_id}
        })
        
        response = controller(request)
        
        assert response.status_code == 400
        assert response.body == "The field 'project_id' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_delete_project_controller_forbidden(self):
        project_repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteProjectUsecase(project_repo, user_repo)
        controller = DeleteProjectController(usecase)
        
        project_id = str(project_repo.projects[0].id)
        normal_user_id = str(user_repo.users[1].id)
        
        request = HttpRequest(body={
            "project_id": project_id,
            "user_from_authorizer": {"user_id": normal_user_id}
        })
        
        response = controller(request)
        
        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"
