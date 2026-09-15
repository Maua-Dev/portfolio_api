import uuid

from src.modules.user.auth_user.app.auth_user_viewmodel import AuthUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_AuthUserViewmodel:

    def test_auth_user_viewmodel_created(self):
        user = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000099"),
            email="giulia@maua.br",
            role=RoleEnum.USER,
        )

        viewmodel = AuthUserViewmodel(user, created=True)

        assert viewmodel.user_id == "00000000-0000-0000-0000-000000000099"
        assert viewmodel.user_email == "giulia@maua.br"
        assert viewmodel.user_role == RoleEnum.USER
        assert viewmodel.to_dict() == {
            'user_id': "00000000-0000-0000-0000-000000000099",
            'user_email': "giulia@maua.br",
            'user_role': "User",
            'message': "the user was created successfully"
        }

    def test_auth_user_viewmodel_retrieved(self):
        user = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
            email="soller@maua.br",
            role=RoleEnum.ADMIN,
        )

        viewmodel = AuthUserViewmodel(user, created=False)

        assert viewmodel.to_dict() == {
            'user_id': "00000000-0000-0000-0000-000000000001",
            'user_email': "soller@maua.br",
            'user_role': "Admin",
            'message': "the user was retrieved successfully"
        }
