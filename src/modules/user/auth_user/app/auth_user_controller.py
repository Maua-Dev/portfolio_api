import logging

from .auth_user_usecase import AuthUserUsecase
from .auth_user_viewmodel import AuthUserViewmodel
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import (
    OK,
    BadRequest,
    InternalServerError,
    Unauthorized,
)

logger = logging.getLogger(__name__)


class AuthUserController:
    def __init__(self, usecase: AuthUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        claims = request.data.get(USER_FROM_AUTHORIZER_KEY)
        if claims is None:
            return Unauthorized(body="Usuário não autenticado")

        try:
            user, created = self.usecase(user_from_authorizer=claims)
            return OK(AuthUserViewmodel(user, created).to_dict())
        except EntityError as err:
            return BadRequest(body=err.message)
        except Exception as err:
            logger.error("Falha no auth_user (%s)", type(err).__name__)
            return InternalServerError(body="Erro interno ao autenticar usuário")