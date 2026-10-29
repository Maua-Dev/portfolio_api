import os
import secrets
import time

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.helpers.errors.usecase_errors import EnvVarNotFound
from src.shared.infra.external.jwt.jwt_kms_signer import JwtKmsSigner
from src.shared.infra.external.microsoft.id_token_verifier import MicrosoftIdTokenVerifier
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS


class LoginUsecase:
    def __init__(
        self,
        repo: IUserRepository,
        observability: ObservabilityAWS,
        jwt_signer: JwtKmsSigner | None = None,
        ms_id_token_verifier: MicrosoftIdTokenVerifier | None = None,
    ):
        self.repo = repo
        self.observability = observability
        self.jwt_signer = jwt_signer
        self.ms_id_token_verifier = ms_id_token_verifier

    def __call__(self, id_token: str) -> tuple[str, str]:

        try:
            verifier = self._get_ms_id_token_verifier()
            ms_payload = verifier.verify(id_token)
            user_sub = ms_payload.get("oid")
            user_mail = ms_payload.get("preferred_username") # sim, o email aparece nessa chave
        except (JwtVerificationError, EnvVarNotFound) as e:
            self.observability.log_error(
                f"Falha na verificação do Microsoft id_token: {e}"
            )
            raise JwtVerificationError("Token de autenticação inválido") from e

        # TODO bate o user_sub (variavel linha 31) no nosso banco pra procurar o usuário
        # da o nome pra variável de "user" pra alinha com o código abaixo
        # TODO atribui essa usuário encontrado a variavel user
        
        if not user:
            
            user = self.repo.create_user(
                new_user=User(
                    id=user_sub,
                    email=user_mail,
                )
            )

        access_payload = {
            "user_id": user.user_id,  # ID interno do seu banco
            "role": user.role,  # Permissão (ex: 'admin')
            "exp": int(time.time()) + (30 * 60),  # 30 minutos
        }

        # TODO usa a função _sign_access_token para assinar o payload

        refresh_token = secrets.token_hex(32)

        # self.repo.save_refresh_token(user.user_id, refresh_token) - nao precisa implementar agora

        return access_token, refresh_token, user

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
