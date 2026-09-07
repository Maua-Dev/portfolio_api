import pytest
import os
from uuid import UUID, uuid4
from pydantic.color import Color
from src.shared.domain.entities.project import Project
from src.shared.helpers.errors.usecase_errors import (NoItemsFound, DuplicatedItem)
from src.shared.infra.repositories.project_repository_dynamo import ProjectRepositoryDynamo
from boto3.dynamodb.conditions import Key

class TestProjectRepositoryDynamo:
    def setup_method(self):
        os.environ["STAGE"] = "TEST"
        os.environ["AWS_ACCESS_KEY_ID"] = "fake"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "fake"
        self.repo = ProjectRepositoryDynamo()

        response = self.repo.dynamo.query(
        key_condition_expression=Key("pk").eq("PROJECT")
        )
        for item in response["Items"]:
            self.repo.dynamo.delete_item(
                item["pk"],
                item["sk"]
        )

    def test_create_project(self):
        project = Project(
            id=uuid4(),
            title="Projeto 1",
            description="Descrição projeto 1",
            cell_image="iamgem.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )
        result = self.repo.create_project(project)
        assert result.id == project.id
        assert result.title == project.title
        assert result.description == project.description
        assert result.cell_image == project.cell_image
        assert result.tech_frontend == project.tech_frontend
        assert result.tech_backend == project.tech_backend
        assert result.color == project.color

    def test_get_project(self):
        project = Project(
            id=uuid4(),
            title="Projeto 1",
            description="Descrição projeto 1",
            cell_image="iamgem.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )

        self.repo.create_project(project)
        result = self.repo.get_project(project.id)

        assert result.id == project.id
        assert result.title == project.title
        assert result.description == project.description
        assert result.cell_image == project.cell_image
        assert result.tech_frontend == project.tech_frontend
        assert result.tech_backend == project.tech_backend
        assert result.color == project.color

    def test_get_all_project(self):
        project1 = Project(
            id=uuid4(),
            title="Projeto 1",
            description="Descrição projeto 1",
            cell_image="iamgem.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )
        project2 = Project(
            id=uuid4(),
            title="Projeto 2",
            description="Descrição projeto 2",
            cell_image="iamgem.jpeg",
            tech_frontend="Vue.js",
            tech_backend="Node.js",
            color=Color("#000000")
        )
        self.repo.create_project(project1)
        self.repo.create_project(project2)
        result = self.repo.get_all_project()

        assert len(result) == 2
        assert result[0].id == project1.id
        assert result[1].id == project2.id


    def test_create_duplicate_project(self):
        project = Project(
            id=uuid4(),
            title="Projeto 1",
            description="Descrição projeto 1",
            cell_image="imagem.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )

        self.repo.create_project(project)
        with pytest.raises(DuplicatedItem):
            self.repo.create_project(project)

    def test_get_not_found_project(self):
        project_id = uuid4()

        with pytest.raises(NoItemsFound):
            self.repo.get_project(project_id)

    def test_update_project(self):
        project = Project(
            id=uuid4(),
            title="Projeto 1",
            description="Descrição projeto 1",
            cell_image="imagem.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )

        self.repo.create_project(project)

        project.title = "Projeto Atualizado"
        project.description = "Descrição atualizada"

        result = self.repo.update_project(project)

        assert result.id == project.id
        assert result.title == "Projeto Atualizado"
        assert result.description == "Descrição atualizada"
        assert result.cell_image == project.cell_image
        assert result.tech_frontend == project.tech_frontend
        assert result.tech_backend == project.tech_backend
        assert result.color == project.color

    def test_update_not_found_project(self):
        project = Project(
            id=uuid4(),
            title="Projeto 1",
            description="Descrição projeto 1",
            cell_image="imagem.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )

        with pytest.raises(NoItemsFound):
            self.repo.update_project(project)

    def test_delete_project(self):
        project = Project(
            id=uuid4(),
            title="Projeto 1",
            description="Descrição projeto 1",
            cell_image="imagem.jpeg",
            tech_frontend="React",
            tech_backend="Python",
            color=Color("#FFFFFF")
        )

        self.repo.create_project(project)
        result = self.repo.delete_project(project.id)

        assert result.id == project.id
        assert result.title == project.title
        assert result.description == project.description
        assert result.cell_image == project.cell_image
        assert result.tech_frontend == project.tech_frontend
        assert result.tech_backend == project.tech_backend
        assert result.color == project.color

    def test_delete_not_found_project(self):
        project_id = uuid4()

        with pytest.raises(NoItemsFound):
            self.repo.delete_project(project_id)