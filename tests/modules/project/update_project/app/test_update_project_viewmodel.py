import uuid
from pydantic.color import Color


from src.modules.project.update_project.app.update_project_viewmodel import UpdateProjectViewmodel
from src.shared.domain.entities.project import Project


class TestUpdateProjectViewmodel:

    def test_to_dict(self):
        project = Project(
            id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
            title="Projeto Teste 1",
            description="Descrição projeto teste 1",
            cell_image="imagem_teste1.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )

        viewmodel = UpdateProjectViewmodel(project)
        result = viewmodel.to_dict()

        assert result == {
            'project_id': "00000000-0000-0000-0000-000000000001",
            'project_title': "Projeto Teste 1",
            'project_description': "Descrição projeto teste 1",
            'project_cell_image': "imagem_teste1.jpeg",
            'project_tech_frontend': "React",
            'project_tech_backend': "Python",
            'project_color': "white",
            'message': "the project was updated successfully"
        }