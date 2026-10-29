from typing import Any, Optional

import jwt
from jwt import PyJWKClient

from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.helpers.errors.usecase_errors import EnvVarNotFound


class MicrosoftIdTokenVerifier:
    """Valida id_token OIDC emitido pelo Microsoft Entra ID (Azure AD)."""

    def __init__(
        self,
        client_id: str,
        tenant_id: str,
        jwks_client: Optional[PyJWKClient] = None,
    ):
        if not client_id:
            raise EnvVarNotFound("MS_CLIENT_ID")
        if not tenant_id:
            raise EnvVarNotFound("MS_TENANT_ID")

        self.client_id = client_id
        self.tenant_id = tenant_id
        self.issuer = f"https://login.microsoftonline.com/{tenant_id}/v2.0"
        jwks_url = (
            f"https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys"
        )
        self.jwks_client = jwks_client or PyJWKClient(jwks_url, cache_keys=True)

    def verify(self, id_token: str) -> dict[str, Any]:
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(id_token)
            return jwt.decode(
                id_token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=self.issuer,
            )
        except jwt.PyJWTError as err:
            raise JwtVerificationError(
                f"Invalid Microsoft id_token: {err}"
            ) from err
