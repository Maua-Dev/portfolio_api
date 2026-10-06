from src.modules.project.get_all_projects.app.get_all_projects_usecase import GetAllProjectsUsecase
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock

class Test_GetAllProjectsUsecase:
    def test_get_all_projects_usecase(self):
        repo = ProjectRepositoryMock()
        usecase = GetAllProjectsUsecase(repo=repo)
        projects = usecase()
        assert len(projects) == 3
        assert projects[0].title == "Projeto Teste 1"
