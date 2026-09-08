from uuid import UUID
from pydantic.color import Color
from typing import List
from boto3.dynamodb.conditions import Key
from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.infra.dto.project_dynamo_dto import ProjectDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.dynamo.dynamo_table import DynamoTable
from src.shared.helpers.errors.usecase_errors import (NoItemsFound, DuplicatedItem)
from src.shared.infra.external.dynamo.dynamo_keys import (EntityKind, partition_key, sort_key)
from src.shared.environments import Environments

class ProjectRepositoryDynamo(IProjectRepository):
    def __init__(self):
        envs = Environments.get_envs()
        self.dynamo = DynamoDatasource(
            dynamo_table_name=envs.dynamo_table_name,
            region=envs.region,
            partition_key=envs.dynamo_partition_key,
            sort_key=envs.dynamo_sort_key,
            endpoint_url=envs.dynamo_endpoint_url,
        )

    def get_project(self, project_id: UUID) -> Project:
        response = self.dynamo.get_item(
            partition_key(EntityKind.PROJECT),
            sort_key(project_id, EntityKind.PROJECT),
        )
        if "Item" not in response:
            raise NoItemsFound("project_id")

        return ProjectDynamoDTO.from_dynamo(
            response["Item"]
        ).to_entity()

    def get_all_project(self) -> List[Project]:
        response = self.dynamo.query(
            key_condition_expression=Key("pk").eq(
                partition_key(EntityKind.PROJECT)
            )
        )
        return [
            ProjectDynamoDTO.from_dynamo(item).to_entity()
            for item in response["Items"]
        ]

    def create_project(self, new_project: Project) -> Project:
        response = self.dynamo.get_item(
            partition_key(EntityKind.PROJECT),
            sort_key(new_project.id, EntityKind.PROJECT),
        )
        if "Item" in response:
            raise DuplicatedItem("project_id")

        dto = ProjectDynamoDTO.from_entity(new_project)
        self.dynamo.put_item(
            item=dto.to_dynamo(),
            partition_key=partition_key(EntityKind.PROJECT),
            sort_key=sort_key(new_project.id, EntityKind.PROJECT),
        )

        return new_project

    def delete_project(self, project_id: UUID) -> Project:
        response = self.dynamo.delete_item(
            partition_key(EntityKind.PROJECT),
            sort_key(project_id, EntityKind.PROJECT),
        )
        if "Attributes" not in response:
            raise NoItemsFound("project_id")

        return ProjectDynamoDTO.from_dynamo(
            response["Attributes"]
        ).to_entity()

    def update_project(self, project: Project) -> Project:
        response = self.dynamo.get_item(
            partition_key(EntityKind.PROJECT),
            sort_key(project.id, EntityKind.PROJECT),
        )

        if "Item" not in response:
            raise NoItemsFound("project_id")

        dto = ProjectDynamoDTO.from_entity(project)
        self.dynamo.hard_update_item(
            partition_key=partition_key(EntityKind.PROJECT),
            sort_key=sort_key(project.id, EntityKind.PROJECT),
            item=dto.to_dynamo(),
        )

        return project
