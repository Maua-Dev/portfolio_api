import uuid

from .update_project_usecase import UpdateProjectUsecase
from .update_project_viewmodel import UpdateProjectViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from pydantic.color import Color

class UpdateProjectController:

    def __init__(self, usecase: UpdateProjectUsecase):
        self.UpdateProjectUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('project_id') is None:
                raise MissingParameters('project_id')

            if type(request.data.get('project_id')) != str:
                raise WrongTypeParameter(
                    fieldName = "project_id",
                    fieldTypeExpected = "str",
                    fieldTypeReceived = request.data.get('project_id').__class__.__name__
                )

            try:
                project_id = uuid.UUID(request.data.get('project_id'))
            except ValueError:
                raise EntityError("project_id")


            title = request.data.get("title")
            if title is not None and type(title) != str:
                raise WrongTypeParameter(
                    fieldName = "title",
                    fieldTypeExpected = "str",
                    fieldTypeReceived = title.__class__.__name__
                )

            description = request.data.get("description")
            if description is not None and type(description) != str:
                raise WrongTypeParameter(
                    fieldName = "description",
                    fieldTypeExpected = "str",
                    fieldTypeReceived = description.__class__.__name__
                )

            cell_image = request.data.get("cell_image")
            if cell_image is not None and type(cell_image) != str:
                raise WrongTypeParameter(
                    fieldName = "cell_image",
                    fieldTypeExpected = "str",
                    fieldTypeReceived = cell_image.__class__.__name__
                )

            tech_frontend = request.data.get("tech_frontend")
            if tech_frontend is not None and type(tech_frontend) != str:
                raise WrongTypeParameter(
                    fieldName = "tech_frontend",
                    fieldTypeExpected = "str",
                    fieldTypeReceived = tech_frontend.__class__.__name__
                )

            tech_backend = request.data.get("tech_backend")
            if tech_backend is not None and type(tech_backend) != str:
                raise WrongTypeParameter(
                    fieldName = "tech_backend",
                    fieldTypeExpected = "str",
                    fieldTypeReceived = tech_backend.__class__.__name__
                )

            color = request.data.get("color")
            if color is not None and type(color) != str:
                raise WrongTypeParameter(
                    fieldName = "color",
                    fieldTypeExpected = "str",
                    fieldTypeReceived = color.__class__.__name__
                )

            project = self.UpdateProjectUsecase(
                project_id = project_id,
                title = title,
                description = description,
                cell_image = cell_image,
                tech_frontend = tech_frontend,
                tech_backend = tech_backend,
                color = Color(color) if color is not None else None
            )

            viewmodel = UpdateProjectViewmodel(project)
            return OK(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body = err.message)

        except MissingParameters as err:
            return BadRequest(body = err.message)

        except WrongTypeParameter as err:
            return BadRequest(body = err.message)

        except EntityError as err:
            return BadRequest(body = err.message)

        except Exception as err:
            return InternalServerError(body = err.args[0])