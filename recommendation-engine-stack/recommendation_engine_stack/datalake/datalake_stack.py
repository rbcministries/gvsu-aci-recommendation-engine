from constructs import Construct
from aws_cdk import (
    NestedStack,
    aws_glue as glue,
    aws_lakeformation as lakeformation,
    aws_s3 as s3,
    aws_iam as iam,
    aws_appflow as appflow,
    aws_lambda as _lambda
)

class DatalakeStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Data lake s3 bucket
        data_lake_bucket = s3.Bucket(self, "dataLakeBucket", bucket_name="recommendation_engine_data_lake")

        # s3 bucket for lambda function to transform GA json to parquet
        ga_appflow_bucket = s3.Bucket(self, "transformBucket", bucket_name="ga_appflow_bucket")

        layer = lambda_.LayerVersion(stack, "pandas-parquet",
            code=lambda_.Code.from_asset(path.join(__dirname, "layer-code")),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_6],
            description="Lambda layer to include pandas and pyarrow"
        )

        # Lambda function to transform GA json to parquet
        lambda_transform_function = _lambda.Function(self, "ga-parquet-converter",
            code=_lambda.Code.from_asset(__dirname, 'lambda'),
            handler='lambda_handler.handler',
            runtime=lambda_.Runtime.PYTHON_3_6,
            layers=[layer]
        )

        # Add event listener for s3 bucket
        lambda_transform_function.add_event_source(eventsources.S3EventSource(ga_appflow_bucket,
            events=[s3.EventType.OBJECT_CREATED, s3.EventType.OBJECT_REMOVED],
            filters=[s3.NotificationKeyFilter(prefix="subdir/")]
        ))

        # Add permissions to Lambda function
        lambda_transform_function.attach_inline_policy(iam.Policy(self, "ga-transform-policy",
            statements=[iam.PolicyStatement(
                actions=["s3:GetObject", "s3:PutObject"],
                resources=[ga_appflow_bucket.bucket_arn]
            )]
        ))

        # Declare appflow
        cfn_flow = appflow.CfnFlow(self, "ga-flow",
            destination_flow_config_list=[appflow.CfnFlow.DestinationFlowConfigProperty(
                connector_type="connectorType",
                s3=appflow.CfnFlow.S3DestinationPropertiesProperty(
                bucket_name="bucketName",
            ),
            source_flow_config_property = appflow.CfnFlow.SourceFlowConfigProperty(
                connector_type="Googleanalytics")
        ))

        cfn_connector_profile = appflow.CfnConnectorProfile(self, "MyCfnConnectorProfile",
            connection_mode="connectionMode",
            connector_profile_name="connectorProfileName",
            connector_type="connectorType",

        # Lake formation role
        bucket_role = iam.Role(
            self,
            "dataLakeBucketRole",
            assumed_by=iam.ServicePrincipal("lakeformation.amazonaws.com"),
            description="Role used by lakeformation to access resources.",
            role_name="LakeFormationServiceAccessRole"
        )

        # Grant read write permissions to data lake
        data_lake_bucket.grant_read_write(bucket_role)

        # Connect data lake to s3 bucket
        cfn_resource = lakeformation.CfnResource(
            self,
            "RecommendationDataLake",
            resource_arn=data_lake_bucket.bucket_arn,
            use_service_linked_role=True,
        )