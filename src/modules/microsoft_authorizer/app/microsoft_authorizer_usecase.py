import re
from uuid import UUID

from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.auth.authorizer_user import build_authorizer_user_context
from src.shared.helpers.auth.iam_policy import generate_policy
from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.external.jwt.jwt_kms_verifier import JwtKmsVerifier

# Routes where the user may not exist in our DB yet (first login / self-registration).
_ONBOARDING_PATH_MARKERS = ("/auth",)

_MAUA_EMAIL_REGEX = re.compile(r"^[^@\s]+@maua\.br$", re.IGNORECASE)


class MicrosoftAuthorizerUsecase:
    def __init__(
        self,
        jwt_verifier: JwtKmsVerifier,
        user_repo: IUserRepository,
    ):
        self.jwt_verifier = jwt_verifier
        self.user_repo = user_repo

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
            user_id = UUID(sub)
        except ValueError:
            return generate_policy("user", "Deny", method_arn)

        if not self._is_onboarding_route(method_arn):
            try:
                self.user_repo.get_user(user_id)
            except NoItemsFound:
                return generate_policy("user", "Deny", method_arn)

        # context só com claims do JWT → LambdaHttpRequest.data["user_from_authorizer"]
        return generate_policy(
            sub,
            "Allow",
            method_arn,
            build_authorizer_user_context(sub=sub, mail=mail),
        )

    @staticmethod
    def _is_onboarding_route(method_arn: str) -> bool:
        return any(marker in method_arn for marker in _ONBOARDING_PATH_MARKERS)
