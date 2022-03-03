from constructs import Construct
from aws_cdk import (
    NestedStack,
    aws_glue as glue,
    aws_lakeformation as lakeformation,
    aws_s3 as s3,
    aws_iam as iam,
)

class DatalakeStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        data_lake_bucket = s3.Bucket(self, "dataLakeBucket", bucket_name="recommendation_engine_data_lake")

        bucket_role = iam.Role(
            self, 
            "dataLakeBucketRole", 
            assumed_by=iam.ServicePrincipal("lakeformation.amazonaws.com"),
            description="Role used by lakeformation to access resources.",
            role_name="LakeFormationServiceAccessRole"            
        )

        data_lake_bucket.grant_read_write(bucket_role)

        cfn_resource = lakeformation.CfnResource(
            self, 
            "RecommendationDataLake",
            resource_arn=data_lake_bucket.bucket_arn,
            use_service_linked_role=True,
        )