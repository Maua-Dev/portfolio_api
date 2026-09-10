import uuid

from .auth_user_usecase import AuthUserUsecase
from .auth_user_viewmodel import AuthUserViewmodel
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import (
    BadRequest,
    Conflict,
    Created,
    InternalServerError,
    OK,
    Unauthorized,
)


class AuthUserController:

    def __init__(self, usecase: AuthUserUsecase):
        self.AuthUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            authorizer_user = request.data.get(USER_FROM_AUTHORIZER_KEY)
            if authorizer_user is None:
                raise MissingParameters(USER_FROM_AUTHORIZER_KEY)

            if type(authorizer_user) != dict:
                raise WrongTypeParameter(
                    fieldName=USER_FROM_AUTHORIZER_KEY,
                    fieldTypeExpected="dict",
                    fieldTypeReceived=authorizer_user.__class__.__name__
                )

            sub = authorizer_user.get('sub')
            if sub is None:
                raise MissingParameters('sub')

            if type(sub) != str:
                raise WrongTypeParameter(
                    fieldName="sub",
                    fieldTypeExpected="str",
                    fieldTypeReceived=sub.__class__.__name__
                )

            mail = authorizer_user.get('mail')
            if mail is None:
                raise MissingParameters('mail')

            if type(mail) != str:
                raise WrongTypeParameter(
                    fieldName="mail",
                    fieldTypeExpected="str",
                    fieldTypeReceived=mail.__class__.__name__
                )

            try:
                user_id = uuid.UUID(sub)
            except ValueError:
                raise EntityError("user_id")

            user, created = self.AuthUserUsecase(
                user_id=user_id,
                email=mail
            )

            viewmodel = AuthUserViewmodel(user, created=created)
            if created:
                return Created(viewmodel.to_dict())

            return OK(viewmodel.to_dict())

        except DuplicatedItem as err:
            return Conflict(body=err.message)

        except MissingParameters as err:
            return Unauthorized(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
