from uuid import uuid4

import pytest

from src.shared.domain.entities.session import Session
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.repositories.session_repository_dynamo import SessionRepositoryDynamo


class FakeDynamoDatasource:
    def __init__(self):
        self.items = {}

    @staticmethod
    def _key(partition_key, sort_key):
        return partition_key, sort_key

    def get_item(self, partition_key, sort_key):
        item = self.items.get(self._key(partition_key, sort_key))
        return {"Item": item} if item is not None else {}

    def put_item(self, item, partition_key, sort_key):
        self.items[self._key(partition_key, sort_key)] = dict(item)
        return {}

    def delete_item(self, partition_key, sort_key):
        item = self.items.pop(self._key(partition_key, sort_key), None)
        return {"Attributes": item} if item is not None else {}


@pytest.fixture
def repo():
    repository = SessionRepositoryDynamo.__new__(SessionRepositoryDynamo)
    repository.dynamo = FakeDynamoDatasource()
    return repository


class TestSessionRepositoryDynamo:
    def test_create_and_get_session(self, repo):
        session = Session(refresh_token="refresh-token", user_id=uuid4())

        created = repo.create_session(session)
        retrieved = repo.get_session(session.user_id)

        assert created == session
        assert retrieved == session
        assert len(repo.dynamo.items) == 1

    def test_create_duplicate_session(self, repo):
        session = Session(refresh_token="refresh-token", user_id=uuid4())
        repo.create_session(session)

        with pytest.raises(DuplicatedItem):
            repo.create_session(session)

    def test_get_session_not_found(self, repo):
        with pytest.raises(NoItemsFound):
            repo.get_session(uuid4())

    def test_update_session(self, repo):
        user_id = uuid4()
        repo.create_session(Session(refresh_token="old-token", user_id=user_id))
        updated_session = Session(refresh_token="new-token", user_id=user_id)

        result = repo.update_session(updated_session)

        assert result == updated_session
        assert repo.get_session(user_id) == updated_session
        assert len(repo.dynamo.items) == 1

    def test_update_session_not_found(self, repo):
        session = Session(refresh_token="new-token", user_id=uuid4())

        with pytest.raises(NoItemsFound):
            repo.update_session(session)

    def test_delete_session(self, repo):
        session = Session(refresh_token="refresh-token", user_id=uuid4())
        repo.create_session(session)

        deleted = repo.delete_session(session.user_id)

        assert deleted == session
        assert repo.dynamo.items == {}

    def test_delete_session_not_found(self, repo):
        with pytest.raises(NoItemsFound):
            repo.delete_session(uuid4())
