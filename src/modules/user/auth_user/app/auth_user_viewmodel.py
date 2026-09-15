from src.shared.domain.entities.user import User


class AuthUserViewmodel:
    user_id: str
    user_email: str
    user_role: str
    message: str

    def __init__(self, user: User, created: bool):
        self.user_id = str(user.id)
        self.user_email = user.email
        self.user_role = user.role
        self.message = (
            "the user was created successfully"
            if created
            else "the user was retrieved successfully"
        )

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_email': self.user_email,
            'user_role': self.user_role,
            'message': self.message
        }
