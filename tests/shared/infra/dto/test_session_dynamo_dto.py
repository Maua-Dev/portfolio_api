from uuid import UUID, uuid4

from src.shared.domain.entities.session import Session
from src.shared.infra.dto.session_dynamo_dto import SessionDynamoDTO


class TestSessionDynamoDTO:
    def test_from_entity_to_dynamo(self):
        user_id = UUID("00000000-0000-0000-0000-000000000001")
        session = Session(refresh_token="refresh-token", user_id=user_id)

        item = SessionDynamoDTO.from_entity_to_dynamo(session)

        assert item == {
            "pk": "SESSION",
            "sk": f"SESSION#{user_id}",
            "refresh_token": "refresh-token",
            "user_id": str(user_id),
        }

    def test_from_dynamo_to_entity_strips_storage_keys(self):
        user_id = UUID("00000000-0000-0000-0000-000000000002")
        item = {
            "pk": "SESSION",
            "sk": f"SESSION#{user_id}",
            "refresh_token": "refresh-token",
            "user_id": str(user_id),
        }

        session = SessionDynamoDTO.from_dynamo_to_entity(item)

        assert session == Session(refresh_token="refresh-token", user_id=user_id)
        assert not hasattr(session, "pk")
        assert not hasattr(session, "sk")

    def test_round_trip(self):
        session = Session(refresh_token="refresh-token", user_id=uuid4())

        item = SessionDynamoDTO.from_entity_to_dynamo(session)
        restored = SessionDynamoDTO.from_dynamo_to_entity(item)

        assert restored == session
