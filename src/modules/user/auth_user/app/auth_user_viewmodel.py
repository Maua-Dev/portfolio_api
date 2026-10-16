from src.shared.domain.entities.user import User


class AuthUserViewmodel:
    def __init__(self, user: User, created: bool):
        self.user = user
        self.created = created

    def to_dict(self) -> dict:
        return {
            "user_id": str(self.user.id),
            "user_email": self.user.email,
            "user_role": self.user.role,
            "created": self.created,
            "message": (
                "the user was created successfully"
                if self.created
                else "the user was retrieved successfully"
            ),
        }