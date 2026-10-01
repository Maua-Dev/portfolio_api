from src.shared.domain.entities.user import User


class DeleteUserViewmodel:
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
            'user_role': self.user_role,
            'message': "the user was deleted successfully"
        }
