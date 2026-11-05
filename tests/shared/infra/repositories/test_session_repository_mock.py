from uuid import uuid4

import pytest

from src.shared.domain.entities.session import Session
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock


class TestSessionRepositoryMock:
    def test_create_and_get_session(self):
        repo = SessionRepositoryMock()
        session = Session(refresh_token="refresh-token", user_id=uuid4())

        created = repo.create_session(session)
        retrieved = repo.get_session(session.user_id)

        assert created == session
        assert retrieved == session
        assert len(repo.sessions) == 1

    def test_create_duplicate_session(self):
        repo = SessionRepositoryMock()
        session = Session(refresh_token="refresh-token", user_id=uuid4())
        repo.create_session(session)

        with pytest.raises(DuplicatedItem):
            repo.create_session(session)

    def test_get_session_not_found(self):
        repo = SessionRepositoryMock()

        with pytest.raises(NoItemsFound):
            repo.get_session(uuid4())

    def test_update_session(self):
        repo = SessionRepositoryMock()
        user_id = uuid4()
        repo.create_session(Session(refresh_token="old-token", user_id=user_id))
        updated_session = Session(refresh_token="new-token", user_id=user_id)

        result = repo.update_session(updated_session)

        assert result == updated_session
        assert repo.get_session(user_id) == updated_session
        assert len(repo.sessions) == 1

    def test_update_session_not_found(self):
        repo = SessionRepositoryMock()
        session = Session(refresh_token="new-token", user_id=uuid4())

        with pytest.raises(NoItemsFound):
            repo.update_session(session)

    def test_delete_session(self):
        repo = SessionRepositoryMock()
        session = Session(refresh_token="refresh-token", user_id=uuid4())
        repo.create_session(session)

        deleted = repo.delete_session(session.user_id)

        assert deleted == session
        assert repo.sessions == []

    def test_delete_session_not_found(self):
        repo = SessionRepositoryMock()

        with pytest.raises(NoItemsFound):
            repo.delete_session(uuid4())
