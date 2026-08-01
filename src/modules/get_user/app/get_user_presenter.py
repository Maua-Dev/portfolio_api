from .get_user_controller import GetUserController
from .get_user_usecase import GetUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_user_repo()()
usecase = GetUserUsecase(repo)
controller = GetUserController(usecase)


def get_user_presenter(event):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()


def lambda_handler(event, context):
    response = get_user_presenter(event)
    return response
