from .create_user_usecase import CreateUserUsecase
from .create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, Conflict, Created, InternalServerError


class CreateUserController:

    def __init__(self, usecase: CreateUserUsecase):
        self.CreateUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('email') is None:
                raise MissingParameters('email')

            if type(request.data.get('email')) != str:
                raise WrongTypeParameter(
                    fieldName="email",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('email').__class__.__name__
                )

            if request.data.get('senha_hash') is None:
                raise MissingParameters('senha_hash')

            if type(request.data.get('senha_hash')) != str:
                raise WrongTypeParameter(
                    fieldName="senha_hash",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('senha_hash').__class__.__name__
                )

            role = request.data.get('role')

            if role is None:
                role = RoleEnum.USER.value

            if type(role) != str:
                raise WrongTypeParameter(
                    fieldName="role",
                    fieldTypeExpected="str",
                    fieldTypeReceived=role.__class__.__name__
                )

            user = self.CreateUserUsecase(
                email=request.data.get('email'),
                senha_hash=request.data.get('senha_hash'),
                role=role
            )

            viewmodel = CreateUserViewmodel(user)
            return Created(viewmodel.to_dict())

        except DuplicatedItem as err:
            return Conflict(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
