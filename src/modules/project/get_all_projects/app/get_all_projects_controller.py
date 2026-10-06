from .get_all_projects_usecase import GetAllProjectsUsecase
from .get_all_projects_viewmodel import GetAllProjectsViewmodel
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError

class GetAllProjectsController:
    def __init__(self, usecase: GetAllProjectsUsecase):
        self.GetAllProjectsUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            projects = self.GetAllProjectsUsecase()
            viewmodel = GetAllProjectsViewmodel(projects)
            return OK(viewmodel.to_dict())
        except Exception as err:
            return InternalServerError(body=err.args[0])
