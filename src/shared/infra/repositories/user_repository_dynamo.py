from typing import List
from uuid import UUID

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
    PK_ATTR,
)


class UserRepositoryDynamo(IUserRepository):

    def __init__(self):
        envs = Environments.get_envs()
        self.dynamo = DynamoDatasource(
            dynamo_table_name=envs.dynamo_table_name,
            region=envs.region,
            partition_key=envs.dynamo_partition_key,
            sort_key=envs.dynamo_sort_key,
            endpoint_url=envs.dynamo_endpoint_url,
        )

    def _pk(self) -> str:
        return partition_key(kind=EntityKind.USER)

    def _sk(self, user_id: UUID) -> str:
        return sort_key(id=user_id, kind=EntityKind.USER)

    def get_user(self, id: UUID) -> User:
        resp = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(id),
        )

        if resp.get("Item") is None:
            raise NoItemsFound("id")

        return UserDynamoDTO.from_dynamo_to_entity(resp["Item"])

    def get_user_by_email(self, email: str) -> User:
        normalized = email.strip().casefold()
        for user in self.get_all_user():
            if user.email.strip().casefold() == normalized:
                return user
        raise NoItemsFound("email")

    def get_all_user(self) -> List[User]:
        users = []
        query_options = {"ConsistentRead": True}
        while True:
            response = self.dynamo.query(
                key_condition_expression=Key(PK_ATTR).eq(self._pk()),
                **query_options,
            )
            users.extend(
                UserDynamoDTO.from_dynamo_to_entity(item)
                for item in response.get("Items", [])
            )
            last_key = response.get("LastEvaluatedKey")
            if not last_key:
                return users
            query_options["ExclusiveStartKey"] = last_key

    def create_user(self, new_user: User) -> User:
        # O ID Microsoft é estável. Uma gravação concorrente não pode
        # sobrescrever um cadastro existente, inclusive sua role.
        try:
            self.dynamo.dynamo_table.put_item(
                Item=UserDynamoDTO.from_entity_to_dynamo(new_user),
                ConditionExpression="attribute_not_exists(#pk)",
                ExpressionAttributeNames={"#pk": PK_ATTR},
            )
        except ClientError as err:
            if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise DuplicatedItem("user") from err
            raise
        return new_user

    def delete_user(self, id: UUID) -> User:
        resp = self.dynamo.delete_item(
            partition_key=self._pk(),
            sort_key=self._sk(id),
        )

        if "Attributes" not in resp:
            raise NoItemsFound("id")

        return UserDynamoDTO.from_dynamo_to_entity(resp["Attributes"])

    def update_user(self, user: User) -> User:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(user.id),
        )
        if existing.get("Item") is None:
            raise NoItemsFound("id")

        self.dynamo.put_item(
            item=UserDynamoDTO.from_entity_to_dynamo(user),
            partition_key=self._pk(),
            sort_key=self._sk(user.id),
        )
        return user