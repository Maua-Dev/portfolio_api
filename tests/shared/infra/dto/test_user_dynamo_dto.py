import uuid

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO


class TestUserDynamoDTO:

    def test_from_entity_to_dynamo(self):
        user = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
            email="rubio@maua.br",
            role=RoleEnum.ADMIN,
        )

        item = UserDynamoDTO.from_entity_to_dynamo(user)

        assert item == {
            'pk': 'USER',
            'sk': 'USER#00000000-0000-0000-0000-000000000001',
            'id': '00000000-0000-0000-0000-000000000001',
            'email': 'rubio@maua.br',
            'role': 'Admin'
        }

    def test_from_entity_to_dynamo_serializes_types(self):
        user = User(
            id=uuid.uuid4(),
            email="sakamoto@maua.br",
            role=RoleEnum.USER,
        )

        item = UserDynamoDTO.from_entity_to_dynamo(user)

        assert isinstance(item['id'], str)
        assert isinstance(item['role'], str)
        assert item['sk'] == f"USER#{user.id}"

    def test_from_dynamo_to_entity(self):
        item = {
            'pk': 'USER',
            'sk': 'USER#00000000-0000-0000-0000-000000000002',
            'id': '00000000-0000-0000-0000-000000000002',
            'email': 'sakamoto@maua.br',
            'role': 'User'
        }

        user = UserDynamoDTO.from_dynamo_to_entity(item)

        assert isinstance(user, User)
        assert user.id == uuid.UUID("00000000-0000-0000-0000-000000000002")
        assert user.email == "sakamoto@maua.br"
        assert user.role == RoleEnum.USER

    def test_from_dynamo_to_entity_strips_storage_keys(self):
        item = {
            'pk': 'USER',
            'sk': 'USER#00000000-0000-0000-0000-000000000003',
            'id': '00000000-0000-0000-0000-000000000003',
            'email': 'rubio@maua.br',
            'role': 'Admin'
        }

        user = UserDynamoDTO.from_dynamo_to_entity(item)

        assert not hasattr(user, 'pk')
        assert not hasattr(user, 'sk')

    def test_round_trip_keeps_the_same_user(self):
        user = User(
            id=uuid.uuid4(),
            email="rubio@maua.br",
            role=RoleEnum.ADMIN,
        )

        item = UserDynamoDTO.from_entity_to_dynamo(user)
        restored = UserDynamoDTO.from_dynamo_to_entity(item)

        assert restored == user
