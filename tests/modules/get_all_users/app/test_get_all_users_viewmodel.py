import uuid

from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class TestGetAllUsersViewmodel:

    def test_to_dict(self):
        users = [
            User(
                id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
                email="rubio@maua.br",
                role=RoleEnum.ADMIN,
            ),
            User(
                id=uuid.UUID("00000000-0000-0000-0000-000000000002"),
                email="sakamoto@maua.br",
                role=RoleEnum.USER,
            )
        ]

        viewmodel = GetAllUsersViewmodel(users)
        result = viewmodel.to_dict()

        assert result == {
            'all_users': [
                {
                    'user_id': '00000000-0000-0000-0000-000000000001',
                    'user_email': 'rubio@maua.br',
                    'user_role': 'Admin'
                },
                {
                    'user_id': '00000000-0000-0000-0000-000000000002',
                    'user_email': 'sakamoto@maua.br',
                    'user_role': 'User'
                }
            ],
            'message': "all users were retrieved successfully"
        }

    def test_to_dict_empty_list(self):
        viewmodel = GetAllUsersViewmodel([])
        result = viewmodel.to_dict()

        assert result == {
            'all_users': [],
            'message': "all users were retrieved successfully"
        }

    def test_user_id_is_string(self):
        users = [
            User(
                id=uuid.uuid4(),
                email="sakamoto@maua.br",
                role=RoleEnum.USER,
            )
        ]

        viewmodel = GetAllUsersViewmodel(users)
        result = viewmodel.to_dict()

        assert isinstance(result['all_users'][0]['user_id'], str)
