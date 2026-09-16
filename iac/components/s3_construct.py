from constructs import Construct
from aws_cdk import Duration, RemovalPolicy, Aws
from aws_cdk import aws_cloudfront as cloudfront, aws_cloudfront_origins as origins, aws_s3


class S3Construct(Construct):
    
    entity_assets_bucket: aws_s3.Bucket
    cloudfront_distribution_plans: cloudfront.Distribution
    cloudfront_distribution_subjects: cloudfront.Distribution

    def _build_distribution(
        self,
        distribution_id: str,
        bucket: aws_s3.Bucket,
        stage: str,
        default_ttl: Duration,
    ) -> cloudfront.Distribution:
        cache_policy = cloudfront.CachePolicy(
            self,
            f"{distribution_id}CachePolicy",
            cache_policy_name=f"Portfolio-{distribution_id}-Cache-{stage}",
            comment=f"Cache policy for {distribution_id}",
            min_ttl=Duration.seconds(1),
            max_ttl=Duration.days(365),
            default_ttl=default_ttl,
            enable_accept_encoding_gzip=True,
            enable_accept_encoding_brotli=True,
        )

        origin_request_policy = cloudfront.OriginRequestPolicy(
            self,
            f"{distribution_id}OriginRequestPolicy",
            origin_request_policy_name=f"Portfolio-{distribution_id}-ORP-{stage}",
            comment=f"Origin request policy for {distribution_id}",
            header_behavior=cloudfront.OriginRequestHeaderBehavior.allow_list(
                "Origin",
                "Access-Control-Request-Headers",
                "Access-Control-Request-Method",
            ),
        )

        return cloudfront.Distribution(
            self,
            id=distribution_id,
            comment=f"Portfolio {distribution_id} S3 CDN {stage}",
            price_class=cloudfront.PriceClass.PRICE_CLASS_ALL,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(bucket),
                compress=True,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
                cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD_OPTIONS,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cache_policy,
                origin_request_policy=origin_request_policy,
                response_headers_policy=cloudfront.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS_WITH_PREFLIGHT,
            ),
        )

    def create_bucket_with_distribution(
        self,
        *,
        resource_prefix: str,
        bucket_name: str,
        default_ttl: Duration,
        stage: str,
    ) -> tuple[aws_s3.Bucket, cloudfront.Distribution]:
        bucket = aws_s3.Bucket(
            self,
            f"{resource_prefix}Bucket",
            bucket_name=bucket_name,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=self.removal_policy,
            auto_delete_objects=self.removal_policy == RemovalPolicy.DESTROY,
        )

        distribution = self._build_distribution(
            distribution_id=f"CloudFrontDistribution{resource_prefix}",
            bucket=bucket,
            stage=stage,
            default_ttl=default_ttl,
        )

        return bucket, distribution

    def __init__(self, scope: Construct, construct_id: str, stage: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.stage = stage.lower()
        self.removal_policy = RemovalPolicy.RETAIN if stage.upper() == "PROD" else RemovalPolicy.DESTROY

        identifier = f"2026-{Aws.ACCOUNT_ID}-{Aws.REGION}"

        self.entity_assets_bucket, self.cloudfront_distribution_entity_assets = self.create_bucket_with_distribution(
            resource_prefix="EntityAssets",
            bucket_name=f"portfolio-entity-assets-{self.stage}-{identifier}",
            default_ttl=Duration.seconds(30),
            stage=stage,
        )
        