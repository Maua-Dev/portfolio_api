import pytest
from pydantic import ValidationError
from pydantic.color import Color
from src.modules.project.create_project.app.create_project_usecase import CreateProjectUsecase
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class TestCreateProjectUsecase:
    def test_create_project(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)

        project = usecase(
            title="Projeto teste 1",
            description="Descrição do projeto 1",
            cell_image="imagem1.jpeg",
            tech_frontend="React",
            tech_backend="Node.js",
            color=Color("#FFFFFF")
            )

        assert repo.projects[-1] == project

    def test_create_project_invalid_title(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)

        with pytest.raises(ValidationError):
            usecase(
                title=None,
                description="Descrição do projeto 1",
                cell_image="imagem1.jpeg",
                tech_frontend="React",
                tech_backend="Node.js",
                color=Color("#FFFFFF")
            )

    def test_create_project_invalid_description(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)

        with pytest.raises(ValidationError):
            usecase(
                title="Test Project 1",
                description=None,
                cell_image="imagem1.jpeg",
                tech_frontend="React",
                tech_backend="Node.js",
                color=Color("#FFFFFF")                
            )
        
    def test_create_project_invalid_cell_image(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)

        with pytest.raises(ValidationError):
            usecase(
                title="Projeto teste 1",
                description="Descrição do projeto 1",
                cell_image=None,
                tech_frontend="React",
                tech_backend="Node.js",
                color=Color("#FFFFFF")
            )

    def test_create_project_invalid_tech_frontend(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)

        with pytest.raises(ValidationError):
            usecase(
                title="Projeto teste 1",
                description="Descrição do projeto 1",
                cell_image="imagem1.jpeg",
                tech_frontend=None,
                tech_backend="Node.js",
                color=Color("#FFFFFF")
            )

    def test_create_project_invalid_tech_backend(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)

        with pytest.raises(ValidationError):
            usecase(
                title="Projeto teste 1",
                description="Descrição do projeto 1",
                cell_image="imagem1.jpeg",
                tech_frontend="React",
                tech_backend=None,
                color=Color("#FFFFFF")
            )

    def test_create_project_invalid_color(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)

        with pytest.raises(ValidationError):
            usecase(
                title="Projeto teste 1",
                description="Descrição do projeto 1",
                cell_image="imagem1.jpeg",
                tech_frontend="React",
                tech_backend="Node.js",
                color=None
            )

