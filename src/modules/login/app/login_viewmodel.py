from src.shared.domain.entities.user import User


class LoginViewmodel:
    def __init__(self, access_token: str, user: User):
        self.access_token = access_token
        role = user.role
        email = user.email
        self.user_role = role.value if hasattr(role, "value") else role
        self.message = "Login successful"

    def to_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "user": {
                "email": self.email,
                "role": self.user_role,
            },
            "message": self.message,
        }
