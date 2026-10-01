from aws_cdk import aws_apigateway as apigateway
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors, CorsOptions

class ApigwConstruct(Construct):
    rest_api: RestApi
    
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        stage: str, 
        **kwargs
    ):
        
        super().__init__(scope, construct_id, **kwargs)
        
        self.stage = stage
        
        cors_options = CorsOptions(
            allow_origins=Cors.ALL_ORIGINS,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "QUERY"],
            allow_headers=Cors.DEFAULT_HEADERS
        )
        
        self.rest_api = RestApi(
            self, 
            id=f"Portfolio_RestApi_{self.stage}",
            rest_api_name=f"Portfolio_RestApi_{self.stage}",
            description=f"This is the Portfolio RestApi for {self.stage}",
            deploy_options=apigateway.StageOptions(
                stage_name=stage.lower(),
                logging_level=apigateway.MethodLoggingLevel.OFF,
                data_trace_enabled=False,
                metrics_enabled=True,
            ),
            default_cors_preflight_options=cors_options,
        )
        
        # implementação de uma key para mínima proteção de rotas abertas sensíveis
        # não precisa ser necessariamente usado
        
        api_key = self.rest_api.add_api_key(
            id="AdminApiKey",
            api_key_name="portfolio-apigw-admin-key"
        )
        
        plan = self.rest_api.add_usage_plan("UsagePlan",
            name="AdminPlan",
            api_stages=[apigateway.UsagePlanPerApiStage(
                api=self.rest_api,
                stage=self.rest_api.deployment_stage,
            )]
        )
        plan.add_api_key(api_key)

        self.api_gateway_resource = self.rest_api.root.add_resource(
            path_part="portfolio",
            default_cors_preflight_options=cors_options
        )