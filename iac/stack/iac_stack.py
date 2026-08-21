import os
from aws_cdk import (
    Stack
)
from constructs import Construct

from components.apigw_construct import ApigwConstruct
from components.dynamo_construct import DynamoConstruct
from components.lambda_construct import LambdaConstruct
from components.s3_construct import S3Construct
from components.ssm_construct import SsmConstruct

class IacStack(Stack):

    def __init__(
        self, 
        scope: Construct,
        stack_id: str,
        stack_name: str,
        stage: str,
        **kwargs
    ) -> None:
        
        super().__init__(scope, stack_id, **kwargs)

        self.github_ref_name = os.environ.get("GITHUB_REF_NAME", "")
        self.aws_region = os.environ.get("AWS_REGION")

        self.apigw_construct = ApigwConstruct(
            self, 
            construct_id=f"Apigw", 
            stage=stage
        )
        
        self.s3_construct = S3Construct(
            self, 
            construct_id=f"S3", 
            stage=stage
        )

        self.dynamo_construct = DynamoConstruct(
            self,
            construct_id=f"Dynamo",
            stack_name=stack_name,
            stage=stage,
        )

        # alinhado com Environments.load_envs() (stages DEV/HOMOLOG/PROD)
        ENVIRONMENT_VARIABLES = {
            "STAGE": stage.upper(),
            "REGION": self.region,
            "DYNAMO_TABLE_NAME": self.dynamo_construct.portfolio_table.table_name,
            "DYNAMO_PARTITION_KEY": "pk",
            "DYNAMO_SORT_KEY": "sk",
            "MSS_NAME": stack_name,
            "ENTITY_ASSETS_BUCKET_NAME": self.s3_construct.entity_assets_bucket.bucket_name,
        }

        self.lambda_construct = LambdaConstruct(
            self,
            construct_id=f"Lambda",
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            stage=stage,
            stack_name=stack_name,
            environment_variables=ENVIRONMENT_VARIABLES
        )
        
        for function in self.lambda_construct.funtions_that_need_dynamo_db_access:
            self.dynamo_construct.portfolio_table.grant_read_write_data(function)
            
        for function in self.lambda_construct.functions_that_need_s3_access:
            self.s3_construct.entity_assets_bucket.grant_read_write(function)
       
        
        # instância SSM manager para passar automaticamente variáveis a um hub de segredos
        # da prórpia conta, evitando ter que manualmente passa-las para o github secrets
        
        # isso evita problemas de discrepância nos endpoints
        
        # atenção aqui, isso deve suprir ao que estamos precisando / pegando de variáveis de 
        # ambiente no CD do front
        
        # nesse projeto nao vamos passar cdn pois o acesso vai vir pela entidade retornada ao
        # inves de um link fixo tipo no antigo dev medias
        
        self.ssm_construct = SsmConstruct(
            self, 
            construct_id=f"Ssm",
            mss_name_identification_for_path="portfolio",
            api=self.apigw_construct.rest_api,
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            buckets=None, # o que deve ser salvo são os CDNs, visto que os buckets bloqueiam acesso pela URL publica
            extra_params=None,
            stage=stage
        )