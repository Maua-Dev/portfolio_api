import uuid

from pydantic_extra_types.color import Color

import pytest


from src.modules.project.update_project.app.update_project_usecase import UpdateProjectUsecase
from src.shared.domain.entities.project import Project
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock



class TestUpdateProjectUsecase:

    def test_update_project_success(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo)
        project_id = repo.projects[0].id

        updated_project = usecase(
            project_id = project_id,
            title = "Novo Titulo",
            description = "Nova descrição",
            cell_image = "novo.jpeg",
            tech_frontend = "Vue",
            tech_backend = "Node",
            color = "#123456"
        )

        assert isinstance(updated_project, Project)
        assert updated_project.id == project_id
        assert updated_project.title == "Novo Titulo"
        assert updated_project.description == "Nova descrição"
        assert updated_project.cell_image == "novo.jpeg"
        assert updated_project.tech_frontend == "Vue"
        assert updated_project.tech_backend == "Node"
        assert updated_project.color == Color("#123456")


    def test_update_project_wrong_type(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo)

        with pytest.raises(EntityError):
            usecase(project_id = "project_id")


    def test_update_project_not_found(self):
        repo =ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo)

        with pytest.raises(NoItemsFound):
            usecase(project_id = uuid.uuid4())
         
            
    def test_update_project_partial(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo)
        original = repo.projects[0]

        project_id = original.id
        old_description = original.description
        old_cell_image = original.cell_image
        old_tech_frontend = original.tech_frontend
        old_tech_backend = original.tech_backend
        old_color = original.color

        updated_project = usecase(project_id = project_id, title = "título mudou")

        assert updated_project.title == "título mudou"
        assert updated_project.description == old_description
        assert updated_project.cell_image == old_cell_image
        assert updated_project.tech_frontend == old_tech_frontend
        assert updated_project.tech_backend == old_tech_backend
        assert updated_project.color == old_color


    def test_update_project_invalid_color(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo)

        with pytest.raises(EntityError):
            usecase(project_id = repo.projects[0].id, color = "xyz")