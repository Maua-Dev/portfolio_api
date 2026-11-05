from uuid import UUID

from src.shared.domain.entities.session import Session
from src.shared.domain.repositories.session_repository_interface import (
    ISessionRepository,
)
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import (
    DuplicatedItem,
    NoItemsFound,
)
from src.shared.infra.dto.session_dynamo_dto import SessionDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import (
    DynamoDatasource,
)
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
)


class SessionRepositoryDynamo(ISessionRepository):

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
        return partition_key(kind=EntityKind.SESSION)

    def _sk(self, user_id: UUID) -> str:
        return sort_key(
            id=user_id,
            kind=EntityKind.SESSION
        )

    def get_session(self, user_id: UUID) -> Session:
        response = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(user_id),
        )

        if response.get("Item") is None:
            raise NoItemsFound("user_id")

        return SessionDynamoDTO.from_dynamo_to_entity(
            response["Item"]
        )

    def create_session(self, session: Session) -> Session:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(session.user_id),
        )

        if existing.get("Item") is not None:
            raise DuplicatedItem("user_id")

        self.dynamo.put_item(
            item=SessionDynamoDTO.from_entity_to_dynamo(session),
            partition_key=self._pk(),
            sort_key=self._sk(session.user_id),
        )

        return session

    def update_session(self, session: Session) -> Session:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(session.user_id),
        )

        if existing.get("Item") is None:
            raise NoItemsFound("user_id")

        self.dynamo.put_item(
            item=SessionDynamoDTO.from_entity_to_dynamo(session),
            partition_key=self._pk(),
            sort_key=self._sk(session.user_id),
        )

        return session

    def delete_session(self, user_id: UUID) -> Session:
        response = self.dynamo.delete_item(
            partition_key=self._pk(),
            sort_key=self._sk(user_id),
        )

        if "Attributes" not in response:
            raise NoItemsFound("user_id")

        return SessionDynamoDTO.from_dynamo_to_entity(
            response["Attributes"]
        )