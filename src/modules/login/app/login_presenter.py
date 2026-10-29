
from .login_controller import LoginController
from .login_usecase import LoginUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler

observability = Environments.get_observability()(module_name="login")

repo = Environments.get_user_repo()()
usecase = LoginUsecase(repo, observability=observability)
controller = LoginController(usecase, observability=observability)


@observed_handler("login")
def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )
    return http_response.toDict()
