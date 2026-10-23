from typing import List

from src.shared.domain.entities.user import User


class UserViewmodel:
    user_id: str
    user_email: str
    user_role: str

    def __init__(self, user: User):
        self.user_id = str(user.id)
        self.user_email = user.email
        self.user_role = user.role

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_email': self.user_email,
            'user_role': self.user_role
        }


class GetAllUsersViewmodel:
    def __init__(self, users_list: List[User]):
        self.users_viewmodel_list = [UserViewmodel(user) for user in users_list]

    def to_dict(self):
        return {
            'all_users': [viewmodel.to_dict() for viewmodel in self.users_viewmodel_list],
            'message': "all users were retrieved successfully"
        }
