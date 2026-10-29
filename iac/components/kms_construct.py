
from aws_cdk import aws_kms as kms
from constructs import Construct


class KMSConstruct(Construct):
    
    jwt_sign_key: kms.Key
    
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kwargs,
    ) -> None:
        
        super().__init__(scope, construct_id, **kwargs)
        
        #TODO add self.jwt_sign_key = kms.Key(...) 
        # - chave que vai ser usada pra gente assinar os jwts na rota de login e verificar assinaturas no authorizer