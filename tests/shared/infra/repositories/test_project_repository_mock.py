import pytest
from pydantic.color import Color
from src.shared.domain.entities.project import Project
from src.shared.helpers.errors.usecase_errors import (NoItemsFound, DuplicatedItem)
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_ProjectRepositoryMock:
    def test_get_project(self):
        repo = ProjectRepositoryMock()
        project = repo.get_project(repo.projects[0].id)
        assert project.title == "Projeto Teste 1"
        assert project.description == "Descrição projeto teste 1"
        assert project.cell_image == "imagem_teste1.jpeg"
        assert project.tech_frontend == "React"
        assert project.tech_backend == "Python"

    def test_get_project_not_found(self):
        repo = ProjectRepositoryMock()
        
        project = Project(
            title="Projeto",
            description="Descrição",
            cell_image="teste.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )

        with pytest.raises(NoItemsFound):
            repo.get_project(project.id)

    def test_get_all_project(self):
        repo = ProjectRepositoryMock()

        projects = repo.get_all_project()

        assert len(projects) == 3

    def test_create_project(self):
        repo = ProjectRepositoryMock()

        project = Project(
            title="Novo Projeto",
            description="Nova descrição",
            cell_image="novo.jpeg",
            tech_frontend="CSS",
            tech_backend="JavaScript",
            color=Color("#123456")
        )

        repo.create_project(project)

        assert repo.projects[3].title == "Novo Projeto"
        assert repo.projects[3].description == "Nova descrição"
        assert repo.projects[3].cell_image == "novo.jpeg"
        assert repo.projects[3].tech_frontend == "CSS"
        assert repo.projects[3].tech_backend == "JavaScript"
        assert repo.projects[3].color == Color("#123456")

    def test_create_project_duplicated(self):
        repo = ProjectRepositoryMock()

        duplicated = repo.projects[0]

        with pytest.raises(DuplicatedItem):
            repo.create_project(duplicated)

    def test_delete_project(self):
        repo = ProjectRepositoryMock()

        project = repo.delete_project(repo.projects[0].id)

        assert project.title == "Projeto Teste 1"
        assert project.description == "Descrição projeto teste 1"
        assert project.cell_image == "imagem_teste1.jpeg"
        assert project.tech_frontend == "React"
        assert project.tech_backend == "Python"
        assert project.color == Color("#FFFFFF")

    def test_delete_project_not_found(self):
        repo = ProjectRepositoryMock()

        project = Project(
            title="Projeto",
            description="Descrição",
            cell_image="teste.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )

        with pytest.raises(NoItemsFound):
            repo.delete_project(project.id)

    def test_update_project(self):
        repo = ProjectRepositoryMock()

        project = repo.projects[0]
        project.title = "Projeto Atualizado"
        updated_project = repo.update_project(project)

        assert updated_project.title == "Projeto Atualizado"
        assert repo.projects[0].title == "Projeto Atualizado"

    def test_update_project_not_found(self):
        repo = ProjectRepositoryMock()

        project = Project(
            title="Projeto",
            description="Descrição",
            cell_image="teste.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )

        with pytest.raises(NoItemsFound):
            repo.update_project(project)