from .get_all_projects_controller import GetAllProjectsController
from .get_all_projects_usecase import GetAllProjectsUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler


repo = Environments.get_project_repo()()
usecase = GetAllProjectsUsecase(repo)
controller = GetAllProjectsController(usecase)


def get_all_projects_presenter(event):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()


@observed_handler("get_all_projects")
def lambda_handler(event, context):
    response = get_all_projects_presenter(event)
    return response
