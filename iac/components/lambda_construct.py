from pathlib import Path

from aws_cdk import Duration, aws_apigateway as apigw, aws_lambda as lambda_
from constructs import Construct

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class LambdaConstruct(Construct):
    def create_lambda_api_gateway_integration(
        self,
        module_name: str,
        method: str,
        api_resource: apigw.Resource,
        api_key_required: bool = False,
        environment_variables: dict | None = None,
        public: bool = False,
        subfolder: str = "",
        authorizer: apigw.TokenAuthorizer | None = None,
    ) -> lambda_.Function:
        module_path = PROJECT_ROOT / "src" / "modules"
        if subfolder:
            module_path /= subfolder
        module_path /= module_name

        function = lambda_.Function(
            self,
            module_name.title(),
            code=lambda_.Code.from_asset(str(module_path)),
            handler=f"app.{module_name}_presenter.lambda_handler",
            function_name=f"{module_name}-{self.stack_name}-{self.stage}"[:63],
            runtime=lambda_.Runtime.PYTHON_3_13,
            architecture=lambda_.Architecture.X86_64,
            layers=[self.lambda_layer],
            environment=(
                environment_variables
                if environment_variables is not None
                else {"STAGE": "TEST"}
            ),
            timeout=Duration.seconds(30),
            memory_size=512,
        )

        parent = api_resource
        if public:
            parent = (
                api_resource.get_resource("public")
                or api_resource.add_resource("public")
            )

        resource = parent.add_resource(module_name.replace("_", "-"))
        method_options = {
            "api_key_required": api_key_required,
            "authorization_type": apigw.AuthorizationType.NONE,
        }
        if not public and authorizer is not None:
            method_options.update(
                authorization_type=apigw.AuthorizationType.CUSTOM,
                authorizer=authorizer,
            )

        resource.add_method(
            method,
            integration=apigw.LambdaIntegration(function),
            **method_options,
        )
        return function

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stage: str,
        stack_name: str,
        api_gateway_resource: apigw.Resource,
        environment_variables: dict,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.stage = stage
        self.stack_name = stack_name
        self.funtions_that_need_dynamo_db_access: list[lambda_.Function] = []
        self.functions_that_need_s3_access: list[lambda_.Function] = []

        self.lambda_layer = lambda_.LayerVersion(
            self,
            id=f"{stack_name}_LambdaLayer_{stage}",
            layer_version_name=f"{stack_name}-LambdaLayer-{stage}",
            code=lambda_.Code.from_asset(str(PROJECT_ROOT / "iac" / "build")),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_13],
            compatible_architectures=[lambda_.Architecture.X86_64],
        )

        self.microsoft_authorizer_function = lambda_.Function(
            self,
            id="MicrosoftAuthorizerLambda",
            function_name=f"microsoft-authorizer-{stack_name}-{stage}"[:63],
            code=lambda_.Code.from_asset(
                str(PROJECT_ROOT / "src" / "modules" / "microsoft_authorizer")
            ),
            handler="app.microsoft_authorizer_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_13,
            architecture=lambda_.Architecture.X86_64,
            layers=[self.lambda_layer],
            environment={
                "GRAPH_MICROSOFT_ENDPOINT": (
                    environment_variables.get("GRAPH_MICROSOFT_ENDPOINT")
                    or "https://graph.microsoft.com/v1.0/me"
                ),
            },
            timeout=Duration.seconds(15),
            memory_size=512,
        )

        self.microsoft_authorizer = apigw.TokenAuthorizer(
            self,
            id="MicrosoftAuthorizer",
            handler=self.microsoft_authorizer_function,
            identity_source=apigw.IdentitySource.header("Authorization"),
            results_cache_ttl=Duration.seconds(0),
        )

        self.auth_user_function = self.create_lambda_api_gateway_integration(
            module_name="auth_user",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            subfolder="user",
            authorizer=self.microsoft_authorizer,
        )
        self.funtions_that_need_dynamo_db_access.append(self.auth_user_function)

        # self.contact_us = self.create_lambda_api_gateway_integration(
        #     module_name="contact_us",
        #     method="POST",
        #     api_resource=api_gateway_resource,
        #     environment_variables=environment_variables,
        #     public=True
        # )

        # ses_send_policy = iam.PolicyStatement(
        #     effect=iam.Effect.ALLOW,
        #     actions=["ses:SendEmail"],
        #     resources=["*"],
        #     conditions={
        #         "StringEquals": {
        #             "ses:FromAddress": environment_variables.get("FROM_EMAIL")
        #         }
        #     }
        # )
        # self.contact_us.add_to_role_policy(ses_send_policy)

        # self.grade_optimizer_function = self.create_lambda_api_gateway_integration(
        #     module_name="grade_optmizer",
        #     method="POST",
        #     api_resource=api_gateway_resource,
        #     environment_variables=environment_variables
        # )

        # self.get_all_disciplinas_function = self.create_lambda_api_gateway_integration(
        #     module_name="get_all_disciplinas",
        #     method="GET",
        #     api_resource=api_gateway_resource,
        #     environment_variables=environment_variables,
        #     subfolder="disciplina"
        # )

        # self.create_curso_function = self.create_lambda_api_gateway_integration(
        #     module_name="create_curso",
        #     method="POST",
        #     api_resource=api_gateway_resource,
        #     environment_variables=environment_variables,
        #     subfolder="curso",
        #     api_key_required=True
        # )

        # self.funtions_that_need_dynamo_db_access.append(self.grade_optimizer_function)
