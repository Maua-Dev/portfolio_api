from pydantic.color import Color
from src.shared.helpers.errors.controller_errors import (MissingParameters, WrongTypeParameter)
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import (Created, BadRequest, NotFound, InternalServerError)
from src.shared.helpers.external_interfaces.external_interface import (IRequest, IResponse)
from .create_project_usecase import CreateProjectUsecase
from .create_project_viewmodel import CreateProjectViewmodel

class CreateProjectController:
    def __init__(self, usecase: CreateProjectUsecase):
        self.CreateProjectUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('title') is None:
                raise MissingParameters('title')
            if request.data.get('description') is None:
                raise MissingParameters('description')
            if request.data.get('cell_image') is None:
                raise MissingParameters('cell_image')
            if request.data.get('tech_frontend') is None:
                raise MissingParameters('tech_frontend')
            if request.data.get('tech_backend') is None:
                raise MissingParameters('tech_backend')
            if request.data.get('color') is None:
                raise MissingParameters('color')


            project = self.CreateProjectUsecase(
                title=request.data.get('title'),
                description=request.data.get('description'),
                cell_image=request.data.get('cell_image'),
                tech_frontend=request.data.get('tech_frontend'),
                tech_backend=request.data.get('tech_backend'),
                color=Color(request.data.get('color'))
            )

            viewmodel = CreateProjectViewmodel(project)
            return Created(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except WrongTypeParameter as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])