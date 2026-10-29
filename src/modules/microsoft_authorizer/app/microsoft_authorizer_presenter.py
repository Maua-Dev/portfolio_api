import os

from .microsoft_authorizer_usecase import MicrosoftAuthorizerUsecase
from src.shared.environments import Environments
from src.shared.helpers.auth.iam_policy import generate_policy
from src.shared.helpers.observability.wrap_handler import observed_handler
from src.shared.infra.external.jwt.jwt_kms_verifier import JwtKmsVerifier

user_repo = Environments.get_user_repo()()
jwt_verifier = JwtKmsVerifier(key_arn=os.environ.get("JWT_SIGN_KEY_ARN", ""))
usecase = MicrosoftAuthorizerUsecase(
    jwt_verifier=jwt_verifier,
    user_repo=user_repo,
)


@observed_handler("microsoft_authorizer")
def lambda_handler(event, context):
    """
    API Gateway TOKEN authorizer.

    Verifies the Bearer JWT against KMS (JWT_SIGN_KEY_ARN), enforces @maua.br,
    and (except onboarding routes) checks that the user exists in our DB.
    """
    method_arn = event.get("methodArn", "*")

    try:
        authorization_token = event["authorizationToken"]
        return usecase(
            authorization_token=authorization_token,
            method_arn=method_arn,
        )
    except Exception as err:
        print(f"Microsoft authorizer error: {err}")
        return generate_policy("user", "Deny", method_arn)
