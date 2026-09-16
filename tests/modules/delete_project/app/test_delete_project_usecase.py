import pytest
from src.modules.delete_project.app.delete_project_usecase import DeleteProjectUsecase
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound

class TestDeleteProjectUsecase:
    def test_delete_project_success(self):
        project_repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteProjectUsecase(repo=project_repo, user_repo=user_repo)
        
        project_id = str(project_repo.projects[0].id)
        # Using Admin user id
        admin_user_id = str(user_repo.users[0].id)
        
        user_from_authorizer = {"user_id": admin_user_id}
        
        project = usecase(project_id=project_id, user_from_authorizer=user_from_authorizer)
        
        assert str(project.id) == project_id

    def test_delete_project_forbidden_role(self):
        project_repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteProjectUsecase(repo=project_repo, user_repo=user_repo)
        
        project_id = str(project_repo.projects[0].id)
        # Using Normal user id
        normal_user_id = str(user_repo.users[1].id)
        
        user_from_authorizer = {"user_id": normal_user_id}
        
        with pytest.raises(ForbiddenAction):
            usecase(project_id=project_id, user_from_authorizer=user_from_authorizer)

    def test_delete_project_missing_user_id(self):
        project_repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteProjectUsecase(repo=project_repo, user_repo=user_repo)
        
        project_id = str(project_repo.projects[0].id)
        user_from_authorizer = {}
        
        with pytest.raises(ForbiddenAction):
            usecase(project_id=project_id, user_from_authorizer=user_from_authorizer)

    def test_delete_project_project_not_found(self):
        project_repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = DeleteProjectUsecase(repo=project_repo, user_repo=user_repo)
        
        # Valid uuid but not existing
        project_id = "00000000-0000-0000-0000-000000000000"
        admin_user_id = str(user_repo.users[0].id)
        
        user_from_authorizer = {"user_id": admin_user_id}
        
        with pytest.raises(NoItemsFound):
            usecase(project_id=project_id, user_from_authorizer=user_from_authorizer)
