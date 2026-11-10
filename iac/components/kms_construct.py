
from aws_cdk import (
    RemovalPolicy,
    aws_kms as kms,
)
from constructs import Construct

RETAINED_STAGES = {"prod", "homolog"}


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
        
        stage_lower = stage.lower()
        removal_policy = (
            RemovalPolicy.RETAIN if stage_lower in RETAINED_STAGES else RemovalPolicy.DESTROY
        )

        self.jwt_sign_key = kms.Key(
            self,
            id="JwtSignKey",
            alias=f"alias/{stack_name}-jwt-sign-key-{stage_lower}",
            description="KMS key for signing and verifying JWT tokens",
            key_spec=kms.KeySpec.RSA_2048,
            key_usage=kms.KeyUsage.SIGN_VERIFY,
            removal_policy=removal_policy,
        )
