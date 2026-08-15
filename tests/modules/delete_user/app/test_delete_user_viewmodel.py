import uuid

from src.modules.delete_user.app.delete_user_viewmodel import DeleteUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class TestDeleteUserViewmodel:

    def test_to_dict(self):
        user = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
            email="rubio@maua.br",
            role=RoleEnum.ADMIN,
            senha_hash="hash_rubio"
        )

        viewmodel = DeleteUserViewmodel(user)
        result = viewmodel.to_dict()

        assert result == {
            'user_id': '00000000-0000-0000-0000-000000000001',
            'user_email': 'rubio@maua.br',
            'user_role': 'Admin',
            'message': "the user was deleted successfully"
        }

    def test_user_id_is_string_and_hides_sensitive_fields(self):
        user = User(
            id=uuid.uuid4(),
            email="sakamoto@maua.br",
            role=RoleEnum.USER,
            senha_hash="hash_sakamoto"
        )

        viewmodel = DeleteUserViewmodel(user)
        result = viewmodel.to_dict()

        assert isinstance(viewmodel.user_id, str)
        assert result['user_role'] == 'User'
        assert 'senha_hash' not in result
