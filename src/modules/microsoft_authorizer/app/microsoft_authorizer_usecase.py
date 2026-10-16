import re
from uuid import UUID

from src.shared.helpers.auth.authorizer_user import build_authorizer_user_context
from src.shared.helpers.auth.iam_policy import generate_policy
from src.shared.infra.external.microsoft.graph_client import MicrosoftGraphClient


class MicrosoftAuthorizerUsecase:
    def __init__(self, graph_client: MicrosoftGraphClient):
        self.graph_client = graph_client

    def __call__(self, authorization_token: str, method_arn: str) -> dict:
        if not isinstance(authorization_token, str):
            raise ValueError("Authorization inválido")

        match = re.fullmatch(r"Bearer\s+(\S+)", authorization_token.strip(), re.IGNORECASE)
        if match is None:
            raise ValueError("Bearer token ausente ou inválido")

        profile = self.graph_client.get_user_profile(match.group(1))
        sub = profile.get("id")
        mail = profile.get("mail") or profile.get("userPrincipalName")
        name = profile.get("displayName") or ""

        if not isinstance(sub, str) or not isinstance(mail, str):
            return generate_policy("user", "Deny", method_arn)

        sub = sub.strip()
        mail = mail.strip().lower()

        try:
            sub = str(UUID(sub))
        except ValueError:
            return generate_policy("user", "Deny", method_arn)

        if re.fullmatch(r"[^@\s]+@maua\.br", mail) is None:
            return generate_policy("user", "Deny", method_arn)

        if not isinstance(name, str):
            name = ""

        return generate_policy(
            principal_id=sub,
            effect="Allow",
            method_arn=method_arn,
            context=build_authorizer_user_context(
                sub=sub, mail=mail, name=name.strip()
            ),
        )