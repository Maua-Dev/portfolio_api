import pytest
from pydantic import ValidationError
from pydantic.color import Color
from src.modules.create_project.app.create_project_viewmodel import CreateProjectViewmodel
from src.shared.domain.entities.project import Project

class TestCreateProjectViewmodel:
    def test_create_project_viewmodel(self):
        project = Project(
            title="Projeto teste 1",
            description="Descrição do projeto 1",
            cell_image="imagem1.jpeg",
            tech_frontend="React",
            tech_backend="Node.js",
            color=Color("#FFFFFF")
        )

        projectViewmodel = CreateProjectViewmodel(project)
        result = projectViewmodel.to_dict()

        expected ={
            'id': str(project.id),
            'title': "Projeto teste 1",
            'description': "Descrição do projeto 1",
            'cell_image': "imagem1.jpeg",
            'tech_frontend': "React",
            'tech_backend': "Node.js",
            'color': "#FFFFFF",
            'message': "the project was created successfully"
        }

        assert expected == result