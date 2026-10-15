from unittest.mock import Mock

import pytest
from botocore.exceptions import ClientError

from src.shared.domain.entities.user import User
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo


def make_repo():
    # Sem credenciais, rede ou DynamoDB Local.
    repo = object.__new__(UserRepositoryDynamo)
    repo.dynamo = Mock()
    return repo


def test_get_user_by_id():
    repo = make_repo()
    user = User(email="leo@maua.br", role="Admin")
    repo.dynamo.get_item.return_value = {
        "Item": UserDynamoDTO.from_entity_to_dynamo(user)
    }

    assert repo.get_user(user.id) == user
    repo.dynamo.get_item.assert_called_once_with(
        partition_key=repo._pk(),
        sort_key=repo._sk(user.id),
    )


def test_get_user_by_id_not_found():
    repo = make_repo()
    user = User(email="missing@maua.br")
    repo.dynamo.get_item.return_value = {}

    with pytest.raises(NoItemsFound):
        repo.get_user(user.id)

    repo.dynamo.get_item.assert_called_once_with(
        partition_key=repo._pk(),
        sort_key=repo._sk(user.id),
    )


def test_create_uses_conditional_write():
    repo = make_repo()
    user = User(email="leo@maua.br")
    assert repo.create_user(user) == user
    kwargs = repo.dynamo.dynamo_table.put_item.call_args.kwargs
    assert kwargs["Item"] == UserDynamoDTO.from_entity_to_dynamo(user)
    assert kwargs["ConditionExpression"] == "attribute_not_exists(#pk)"


def test_conditional_failure_does_not_overwrite_user():
    repo = make_repo()
    repo.dynamo.dynamo_table.put_item.side_effect = ClientError(
        {"Error": {"Code": "ConditionalCheckFailedException"}}, "PutItem"
    )
    with pytest.raises(DuplicatedItem):
        repo.create_user(User(email="leo@maua.br"))


def test_other_dynamo_errors_are_not_hidden():
    repo = make_repo()
    repo.dynamo.dynamo_table.put_item.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException"}}, "PutItem"
    )
    with pytest.raises(ClientError):
        repo.create_user(User(email="leo@maua.br"))