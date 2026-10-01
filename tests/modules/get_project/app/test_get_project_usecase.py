import uuid

import pytest

from src.modules.get_project.app.get_project_usecase import GetProjectUsecase
from src.shared.domain.entities.project import Project
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock



class TestGetProjectUsecase:

    def test_get_project_success(self):
        repo = ProjectRepositoryMock()
        usecase = GetProjectUsecase(repo)

        project = usecase(project_id=repo.projects[0].id)

        assert isinstance(project, Project)
        assert project.id == repo.projects[0].id
        assert project.title == "Projeto Teste 1"
        assert project.description == "Descrição projeto teste 1"
        assert project.cell_image == "imagem_teste1.jpeg"
        assert project.tech_frontend == "React"
        assert project.tech_backend == "Python"

    def test_get_project_not_found(self):
        repo = ProjectRepositoryMock()
        usecase = GetProjectUsecase(repo)

        with pytest.raises(NoItemsFound):
            usecase(project_id=uuid.uuid4())

    def test_get_project_wrong_type(self):
        repo = ProjectRepositoryMock()
        usecase = GetProjectUsecase(repo)

        with pytest.raises(EntityError):
            usecase(project_id="00000000-0000-0000-0000-000000000001")

        