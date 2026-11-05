from src.shared.domain.entities.session import Session
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
    strip_keys,
)


class SessionDynamoDTO:

    @staticmethod
    def from_entity_to_dynamo(session: Session) -> dict:
        return {
            **session.model_dump(mode="json"),
            "pk": partition_key(kind=EntityKind.SESSION),
            "sk": sort_key(
                id=session.user_id,
                kind=EntityKind.SESSION
            ),
        }

    @staticmethod
    def from_dynamo_to_entity(session_data: dict) -> Session:
        return Session.model_validate(
            obj=strip_keys(session_data)
        )