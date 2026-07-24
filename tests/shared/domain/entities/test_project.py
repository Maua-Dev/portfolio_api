import uuid
import pytest

from pydantic.color import Color
from src.shared.domain.entities.project import Project
from pydantic import ValidationError

class Test_Project:
    def test_project(self):
        Project(
            title="Projeto Teste",
            description="Descrição projeto teste",
            cell_image="imagem_teste.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )

    def test_project_title_is_none(self):
        with pytest.raises(ValidationError):
            Project(
            title=None,
            description="Descrição projeto teste",
            cell_image="imagem_teste.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
            )

    def test_project_description_is_none(self):
        with pytest.raises(ValidationError):
            Project(
            title="Projeto Teste",
            description=None,
            cell_image="imagem_teste.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
            )
    def test_project_cell_image_is_none(self):
        with pytest.raises(ValidationError):
            Project(
            title="Projeto Teste",
            description="Descrição projeto teste",
            cell_image=None,
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
            )
    
    def test_project_tech_frontend_is_none(self):
        with pytest.raises(ValidationError):
            Project(
            title="Projeto Teste",
            description="Descrição projeto teste",
            cell_image="imagem_teste.jpeg",
            tech_frontend=None,
            tech_backend="Python",
            color=Color("#FFFFFF")
            )

    def test_project_tech_backend_is_none(self):
        with pytest.raises(ValidationError):
            Project(
            title="Projeto Teste",
            description="Descrição projeto teste",
            cell_image="imagem_teste.jpeg",
            tech_frontend="React",
            tech_backend=None,
            color=Color("#FFFFFF")
            )

    def test_project_color_is_none(self):
        with pytest.raises(ValidationError):
            Project(
            title="Projeto Teste",
            description="Descrição projeto teste",
            cell_image="imagem_teste.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=None
            )