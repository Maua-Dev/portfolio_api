import os

from .microsoft_authorizer_usecase import MicrosoftAuthorizerUsecase
from src.shared.helpers.auth.iam_policy import generate_policy
from src.shared.helpers.observability.wrap_handler import observed_handler
from src.shared.infra.external.jwt.jwt_kms_verifier import JwtKmsVerifier

jwt_verifier = JwtKmsVerifier(key_arn=os.environ.get("JWT_SIGN_KEY_ARN", ""))
usecase = MicrosoftAuthorizerUsecase(jwt_verifier=jwt_verifier)


@observed_handler("microsoft_authorizer")
def lambda_handler(event, context):
    """
    API Gateway TOKEN authorizer.

    Verifies the Bearer access JWT against KMS (JWT_SIGN_KEY_ARN) and enforces
    basic claims (sub UUID + @maua.br mail). Role/authorization stays in usecases.
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
