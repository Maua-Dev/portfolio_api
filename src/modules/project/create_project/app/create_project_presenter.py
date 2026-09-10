from .create_project_controller import CreateProjectController
from .create_project_usecase import CreateProjectUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
import json

repo = Environments.get_project_repo()()
usecase = CreateProjectUsecase(repo)
controller = CreateProjectController(usecase)

def lambda_handler(event, context):
    from pprint import pprint
    pprint(event)

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()