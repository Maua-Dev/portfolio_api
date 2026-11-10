import os
import re
import secrets
import time
from uuid import UUID

from pydantic import ValidationError

from src.shared.domain.entities.session import Session
from src.shared.domain.entities.user import User
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.session_repository_interface import ISessionRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.helpers.errors.usecase_errors import (
    DuplicatedItem,
    EnvVarNotFound,
    ForbiddenAction,
    InvalidJwtFormat,
    NoItemsFound,
)
from src.shared.infra.external.jwt.jwt_kms_signer import JwtKmsSigner
from src.shared.infra.external.jwt.jwt_utils import is_jwt_shape
from src.shared.infra.external.microsoft.id_token_verifier import MicrosoftIdTokenVerifier

_MAUA_EMAIL_REGEX = re.compile(r"^[^@\s]+@maua\.br$", re.IGNORECASE)


class LoginUsecase:
    def __init__(
        self,
        repo: IUserRepository,
        session_repo: ISessionRepository,
        observability: IObservability,
        jwt_signer: JwtKmsSigner | None = None,
        ms_id_token_verifier: MicrosoftIdTokenVerifier | None = None,
    ):
        self.repo = repo
        self.session_repo = session_repo
        self.observability = observability
        self.jwt_signer = jwt_signer
        self.ms_id_token_verifier = ms_id_token_verifier

    def __call__(self, id_token: str) -> tuple[str, str, User]:
        if not is_jwt_shape(id_token):
            raise InvalidJwtFormat("id_token")

        try:
            verifier = self._get_ms_id_token_verifier()
            ms_payload = verifier.verify(id_token)
        except (JwtVerificationError, EnvVarNotFound) as error:
            self.observability.log_exception(
                f"Falha na verificação do Microsoft id_token: {error}"
            )
            raise JwtVerificationError("Token de autenticação inválido") from error

        user_id, user_mail = self._extract_user_claims(ms_payload)

        if not _MAUA_EMAIL_REGEX.fullmatch(user_mail):
            raise ForbiddenAction("email domain")

        user = self._get_or_create_user(user_id=user_id, user_mail=user_mail)

        now = int(time.time())
        role = user.role.value if hasattr(user.role, "value") else user.role
        access_payload = {
            # Esses dois claims são exigidos pelo MicrosoftAuthorizerUsecase.
            "sub": str(user.id),
            "mail": str(user.email),
            # Claims úteis para a aplicação.
            "user_id": str(user.id),
            "role": role,
            "iat": now,
            "exp": now + (30 * 60),
        }
        access_token = self._sign_access_token(access_payload)

        refresh_token = secrets.token_hex(32)
        self._create_or_update_session(
            Session(refresh_token=refresh_token, user_id=user.id)
        )

        return access_token, refresh_token, user

    @staticmethod
    def _extract_user_claims(ms_payload: dict) -> tuple[UUID, str]:
        if not isinstance(ms_payload, dict):
            raise InvalidJwtFormat("Microsoft claims")

        raw_user_id = ms_payload.get("oid")
        user_mail = ms_payload.get("preferred_username")

        if not isinstance(raw_user_id, str) or not raw_user_id.strip():
            raise InvalidJwtFormat("Microsoft oid")
        if not isinstance(user_mail, str) or not user_mail.strip():
            raise InvalidJwtFormat("Microsoft preferred_username")

        try:
            user_id = UUID(raw_user_id)
        except ValueError as error:
            raise InvalidJwtFormat("Microsoft oid") from error

        return user_id, user_mail.strip()

    def _get_or_create_user(self, user_id: UUID, user_mail: str) -> User:
        try:
            return self.repo.get_user(user_id)
        except NoItemsFound:
            try:
                new_user = User(id=user_id, email=user_mail)
            except ValidationError as error:
                raise InvalidJwtFormat("Microsoft user claims") from error

            return self.repo.create_user(new_user=new_user)

    def _create_or_update_session(self, session: Session) -> Session:
        try:
            return self.session_repo.create_session(session)
        except DuplicatedItem:
            # Um usuário possui no máximo uma sessão; um novo login substitui
            # o refresh token anterior.
            return self.session_repo.update_session(session)

    def _get_ms_id_token_verifier(self) -> MicrosoftIdTokenVerifier:
        if self.ms_id_token_verifier is not None:
            return self.ms_id_token_verifier

        return MicrosoftIdTokenVerifier(
            client_id=os.environ.get("MS_CLIENT_ID", ""),
            tenant_id=os.environ.get("MS_TENANT_ID", ""),
        )

    def _sign_access_token(self, payload: dict) -> str:
        signer = self.jwt_signer
        if signer is None:
            key_arn = os.environ.get("JWT_SIGN_KEY_ARN") or os.environ.get(
                "LOGIN_KMS_SIGN_KEY_ARN"
            )
            if not key_arn:
                raise EnvVarNotFound("JWT_SIGN_KEY_ARN")
            signer = JwtKmsSigner(key_arn=key_arn)

        return signer.sign(payload)
