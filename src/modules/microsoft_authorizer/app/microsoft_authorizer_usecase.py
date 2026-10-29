import re
from uuid import UUID

from src.shared.helpers.auth.authorizer_user import build_authorizer_user_context
from src.shared.helpers.auth.iam_policy import generate_policy
from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.infra.external.jwt.jwt_kms_verifier import JwtKmsVerifier

_MAUA_EMAIL_REGEX = re.compile(r"^[^@\s]+@maua\.br$", re.IGNORECASE)


class MicrosoftAuthorizerUsecase:
    def __init__(self, jwt_verifier: JwtKmsVerifier):
        self.jwt_verifier = jwt_verifier

    def __call__(self, authorization_token: str, method_arn: str) -> dict:
        token = authorization_token.replace("Bearer ", "", 1).strip()

        try:
            claims = self.jwt_verifier.verify_and_decode(token)
        except JwtVerificationError:
            return generate_policy("user", "Deny", method_arn)

        sub = str(claims.get("sub") or "").strip()
        mail = str(claims.get("mail") or "").strip()

        if not sub or not mail or not _MAUA_EMAIL_REGEX.match(mail):
            return generate_policy("user", "Deny", method_arn)

        try:
            UUID(sub)
        except ValueError:
            return generate_policy("user", "Deny", method_arn)

        # context só com claims do JWT → LambdaHttpRequest.data["user_from_authorizer"]
        return generate_policy(
            sub,
            "Allow",
            method_arn,
            build_authorizer_user_context(sub=sub, mail=mail),
        )
