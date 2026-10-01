import uuid
from pydantic.color import Color
from src.shared.domain.entities.project import Project
from src.shared.infra.dto.project_dynamo_dto import ProjectDynamoDTO


class TestProjectDynamoDTO:
    def test_from_entity(self):
        project = Project(
            id=uuid.uuid4(),
            title="Projeto dynamo teste",
            description="Descrição do projeto dynamo teste",
            cell_image="imagem.jpeg",
            tech_frontend="React",
            tech_backend="FastAPI",
            color=Color("#FFFFFF"),
        )

        dto = ProjectDynamoDTO.from_entity(project)
        assert dto.id == str(project.id)
        assert dto.title == project.title
        assert dto.description == project.description
        assert dto.cell_image == project.cell_image
        assert dto.tech_frontend == project.tech_frontend
        assert dto.tech_backend == project.tech_backend
        assert dto.color == project.color

        def test_to_dynamo(self):
            project_id = uuid.uuid4()

            dto = ProjectDynamoDTO(
                id=str(project_id),
                title="Projeto dynamo teste",
                description="Descrição do projeto dynamo teste",
                cell_image="imagem.jpeg",
                tech_frontend="React",
                tech_backend="FastAPI",
                color=Color("#FFFFFFF"),
            )
            result = dto.to_dynamo()

            assert result["entity"] == "Project"
            assert result["pk"] == "PROJECT"
            assert result["sk"] == f"PROJECT#{project_id}"
            assert result["id"] == str(project_id)
            assert result["title"] == "Projeto Teste"
            assert result["description"] == "Descrição do projeto"
            assert result["cell_image"] == "imagem.jpeg"
            assert result["tech_frontend"] == "React"
            assert result["tech_backend"] == "FastAPI"

        def test_from_dynamo(self):
            project_id = uuid.uuid4()

            project_data = {
                "entity": "project",
                "pk": "PROJECT",
                "sk": f"PROJECT#{project_id}",
                "id": str(project_id),
                "title": "Projeto Teste",
                "description": "Descrição do projeto",
                "cell_image": "imagem.jpeg",
                "tech_frontend": "React",
                "tech_backend": "FastAPI",
                "color": "#FFFFFF",
            }

            dto = ProjectDynamoDTO.from_dynamo(project_data)

            assert dto.id == str(project_id)
            assert dto.title == "Projeto Teste"
            assert dto.description == "Descrição do projeto"
            assert dto.cell_image == "imagem.jpeg"
            assert dto.tech_frontend == "React"
            assert dto.tech_backend == "FastAPI"
            assert dto.color == Color("#FFFFFF")

        def test_to_entity(self):
            project_id = uuid.uuid4()

            dto = ProjectDynamoDTO(
                id=str(project_id),
                title="Projeto Teste",
                description="Descrição do projeto",
                cell_image="imagem.jpeg",
                tech_frontend="React",
                tech_backend="FastAPI",
                color="#FFFFF",
            )

            project = dto.to_entity()

            assert isinstance(project, Project)
            assert project.id == project_id
            assert project.title == dto.title
            assert project.description == dto.description
            assert project.cell_image == dto.cell_image
            assert project.tech_frontend == dto.tech_frontend
            assert project.tech_backend == dto.tech_backend
            assert project.color == dto.color

