from aws_cdk import (
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    Duration
)
from aws_cdk import aws_iam as iam
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration


class LambdaConstruct(Construct):
    
    stage: str
    stack_name: str
    funtions_that_need_dynamo_db_access: list[lambda_.Function] = []
    functions_that_need_s3_access: list[lambda_.Function] = []

    def create_lambda_api_gateway_integration(
        self, 
        module_name: str,
        method: str, 
        api_resource: Resource,
        api_key_required: bool = False,
        environment_variables: dict = {"STAGE": "TEST"},
        public: bool = False,
        subfolder: str = "",
    ) -> lambda_.Function:
        
        code = lambda_.Code.from_asset(f"../src/modules/{subfolder}/{module_name}") if subfolder else lambda_.Code.from_asset(f"../src/modules/{module_name}")
        handler = f"app.{module_name}_presenter.lambda_handler"
        
        function = lambda_.Function(
            self, module_name.title(),
            code=code,
            handler=handler,
            function_name=f"{module_name}-{self.stack_name}-{self.stage}"[:63],
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(30),
            memory_size=512
        )

        if public:
            api_resource.add_resource("public").add_resource(module_name.replace("_", "-")).add_method(
                method,
                integration=LambdaIntegration(function),
                api_key_required=api_key_required
            )
        else:
            api_resource.add_resource(module_name.replace("_", "-")).add_method(
                method,
                integration=LambdaIntegration(function),
                api_key_required=api_key_required
            )

        return function

    def __init__(
        self, 
        scope: Construct,
        construct_id: str,
        stage: str,
        stack_name: str,
        api_gateway_resource: Resource,
        environment_variables: dict,
        **kargs
    ) -> None:
        
        super().__init__(scope, construct_id, **kargs)
        
        self.stage = stage
        self.stack_name = stack_name

        self.lambda_layer = lambda_.LayerVersion(
            self, 
            id=f"{stack_name}_LambdaLayer_{stage}",
            layer_version_name=f"{stack_name}-LambdaLayer-{self.stage}",
            # a pasta .build foi obtida do adjust layer directory, certifique-se de que a configuração da pasta layer gerada la esta igual
            code=lambda_.Code.from_asset("./build"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_13]
        )
        
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
        