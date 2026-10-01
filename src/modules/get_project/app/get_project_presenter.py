
from src.modules.get_project.app.get_project_controller import GetProjectController
from src.modules.get_project.app.get_project_usecase import GetProjectUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler


repo = Environments.get_project_repo()()
usecase = GetProjectUsecase(repo)
controller = GetProjectController(usecase)


def get_project_presenter(event):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()


@observed_handler("get_project")
def lambda_handler(event, context):
    response = get_project_presenter(event)
    return response
