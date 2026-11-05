from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.helpers.errors.usecase_errors import (
    DuplicatedItem,
    EnvVarNotFound,
    ForbiddenAction,
    InvalidJwtFormat,
    NoItemsFound,
)
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import (
    BadRequest,
    Conflict,
    Forbidden,
    InternalServerError,
    NotFound,
    OK,
    Unauthorized,
)
from src.shared.domain.observability.observability_interface import IObservability

from .login_usecase import LoginUsecase
from .login_viewmodel import LoginViewmodel


_REFRESH_COOKIE_MAX_AGE = 60 * 60 * 24 * 7


class LoginController:
    def __init__(self, usecase: LoginUsecase, observability: IObservability):
        self.usecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            id_token = request.data.get("id_token")
            if id_token is None:
                raise MissingParameters("id_token")
            if not isinstance(id_token, str):
                raise WrongTypeParameter(
                    fieldName="id_token",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(id_token).__name__,
                )

            access_token, refresh_token, user = self.usecase(id_token=id_token)
            viewmodel = LoginViewmodel(access_token=access_token, user=user)

            refresh_cookie = (
                f"refresh_token={refresh_token}; HttpOnly; Secure; SameSite=Strict; "
                f"Path=/; Max-Age={_REFRESH_COOKIE_MAX_AGE}"
            )
            return OK(
                body=viewmodel.to_dict(),
                headers={
                    "Content-Type": "application/json",
                    "Set-Cookie": refresh_cookie,
                },
            )

        except (JwtVerificationError, InvalidJwtFormat) as error:
            self.observability.log_exception(message=error.message)
            return Unauthorized(body=error.message)

        except ForbiddenAction as error:
            self.observability.log_exception(message=error.message)
            return Forbidden(body=error.message)

        except NoItemsFound as error:
            self.observability.log_exception(message=error.message)
            return NotFound(body=error.message)

        except DuplicatedItem as error:
            self.observability.log_exception(message=error.message)
            return Conflict(body=error.message)

        except (MissingParameters, WrongTypeParameter, EntityError) as error:
            self.observability.log_exception(message=error.message)
            return BadRequest(body=error.message)

        except EnvVarNotFound as error:
            self.observability.log_exception(message=error.message)
            return InternalServerError(body=error.message)

        except Exception as error:
            self.observability.log_exception(message=str(error))
            return InternalServerError(body=str(error))
