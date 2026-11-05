from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from src.shared.domain.entities.session import Session


class TestSession:
    def test_create_session(self):
        user_id = uuid4()
        session = Session(refresh_token="refresh-token", user_id=user_id)

        assert session.refresh_token == "refresh-token"
        assert session.user_id == user_id
        assert isinstance(session.user_id, UUID)

    def test_create_session_from_string_uuid(self):
        user_id = str(uuid4())

        session = Session(refresh_token="refresh-token", user_id=user_id)

        assert session.user_id == UUID(user_id)

    def test_create_session_requires_both_fields(self):
        with pytest.raises(ValidationError):
            Session(refresh_token="refresh-token")

        with pytest.raises(ValidationError):
            Session(user_id=uuid4())

    def test_create_session_rejects_extra_fields(self):
        with pytest.raises(ValidationError):
            Session(
                refresh_token="refresh-token",
                user_id=uuid4(),
                extra_field="not-allowed",
            )
