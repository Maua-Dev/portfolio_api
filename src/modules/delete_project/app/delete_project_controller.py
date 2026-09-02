from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, NotFound, InternalServerError, Forbidden
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from .delete_project_usecase import DeleteProjectUsecase
from .delete_project_viewmodel import DeleteProjectViewmodel

class DeleteProjectController:
    def __init__(self, usecase: DeleteProjectUsecase):
        self.DeleteProjectUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('project_id') is None:
                raise MissingParameters('project_id')
                
            if request.data.get('user_from_authorizer') is None:
                raise MissingParameters('user_from_authorizer')

            if not isinstance(request.data.get('project_id'), str):
                raise WrongTypeParameter(
                    'project_id', 'str', type(request.data.get('project_id')).__name__
                )
                
            if not isinstance(request.data.get('user_from_authorizer'), dict):
                raise WrongTypeParameter(
                    'user_from_authorizer', 'dict', type(request.data.get('user_from_authorizer')).__name__
                )

            project = self.DeleteProjectUsecase(
                project_id=request.data.get('project_id'),
                user_from_authorizer=request.data.get('user_from_authorizer')
            )

            viewmodel = DeleteProjectViewmodel(project)
            return OK(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)
            
        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
