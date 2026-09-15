from typing import List

from .get_all_users_usecase import GetAllUsersUsecase
from .get_all_users_viewmodel import GetAllUsersViewmodel
from src.shared.domain.entities.user import User
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class GetAllUsersController:

    def __init__(self, usecase: GetAllUsersUsecase):
        self.GetAllUsersUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            all_users_list: List[User] = self.GetAllUsersUsecase()

            viewmodel = GetAllUsersViewmodel(all_users_list)
            return OK(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
