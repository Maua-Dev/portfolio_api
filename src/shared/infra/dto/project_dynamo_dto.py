from src.shared.domain.entities.project import Project
from src.shared.infra.external.dynamo.dynamo_keys import (strip_keys, EntityKind, partition_key, sort_key)
from pydantic.color import Color
from pydantic import BaseModel
import uuid


class ProjectDynamoDTO(BaseModel):
    id: str
    title: str
    description: str
    cell_image: str
    tech_frontend: str
    tech_backend: str
    color: Color

    @staticmethod
    def from_entity(project: Project) -> "ProjectDynamoDTO":
        return ProjectDynamoDTO.model_validate(project.model_dump())

    def to_dynamo(self) -> dict:
        return {
            "entity": "project",
            "pk": partition_key(EntityKind.PROJECT),
            "sk": sort_key(uuid.UUID(self.id), EntityKind.PROJECT),
            **self.model_dump()
        } 

    @staticmethod
    def from_dynamo(project_data: dict) -> "ProjectDynamoDTO":
        return ProjectDynamoDTO.model_validate(
            strip_keys(project_data)
        )

    def to_entity(self) -> Project:
        return Project.model_validate(self.model_dump())