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

        cfn_delivery_stream = kinesisfirehose.CfnDeliveryStream(self, "MyCfnDeliveryStream",
        amazonopensearchservice_destination_configuration=kinesisfirehose.CfnDeliveryStream.AmazonopensearchserviceDestinationConfigurationProperty(
        index_name="indexName",
        role_arn="roleArn",
        s3_configuration=kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty(
            bucket_arn="bucketArn",
            role_arn="roleArn",

            # the properties below are optional
            buffering_hints=kinesisfirehose.CfnDeliveryStream.BufferingHintsProperty(
                interval_in_seconds=123,
                size_in_mBs=123
            ),
            cloud_watch_logging_options=kinesisfirehose.CfnDeliveryStream.CloudWatchLoggingOptionsProperty(
                enabled=False,
                log_group_name="logGroupName",
                log_stream_name="logStreamName"
            ),
            compression_format="compressionFormat",
            encryption_configuration=kinesisfirehose.CfnDeliveryStream.EncryptionConfigurationProperty(
                kms_encryption_config=kinesisfirehose.CfnDeliveryStream.KMSEncryptionConfigProperty(
                    awskms_key_arn="awskmsKeyArn"
                ),
                no_encryption_config="noEncryptionConfig"
            ),
            error_output_prefix="errorOutputPrefix",
            prefix="prefix"
        ),

        # the properties below are optional
        buffering_hints=kinesisfirehose.CfnDeliveryStream.AmazonopensearchserviceBufferingHintsProperty(
            interval_in_seconds=123,
            size_in_mBs=123
        ),
        cloud_watch_logging_options=kinesisfirehose.CfnDeliveryStream.CloudWatchLoggingOptionsProperty(
            enabled=False,
            log_group_name="logGroupName",
            log_stream_name="logStreamName"
        ),
        cluster_endpoint="clusterEndpoint",
        domain_arn="domainArn",
        index_rotation_period="indexRotationPeriod",
        processing_configuration=kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty(
            enabled=False,
            processors=[kinesisfirehose.CfnDeliveryStream.ProcessorProperty(
                type="type",

                # the properties below are optional
                parameters=[kinesisfirehose.CfnDeliveryStream.ProcessorParameterProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )]
            )]
        ),
        retry_options=kinesisfirehose.CfnDeliveryStream.AmazonopensearchserviceRetryOptionsProperty(
            duration_in_seconds=123
        ),
        s3_backup_mode="s3BackupMode",
        type_name="typeName",
        vpc_configuration=kinesisfirehose.CfnDeliveryStream.VpcConfigurationProperty(
            role_arn="roleArn",
            security_group_ids=["securityGroupIds"],
            subnet_ids=["subnetIds"]
        )
    ),
    delivery_stream_name="deliveryStreamName",
    delivery_stream_type="deliveryStreamType",
    kinesis_stream_source_configuration=kinesisfirehose.CfnDeliveryStream.KinesisStreamSourceConfigurationProperty(
        kinesis_stream_arn="kinesisStreamArn",
        role_arn="roleArn"
    ),
    s3_destination_configuration=kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty(
        bucket_arn="bucketArn",
        role_arn="roleArn",

        # the properties below are optional
        buffering_hints=kinesisfirehose.CfnDeliveryStream.BufferingHintsProperty(
            interval_in_seconds=123,
            size_in_mBs=123
        ),
        cloud_watch_logging_options=kinesisfirehose.CfnDeliveryStream.CloudWatchLoggingOptionsProperty(
            enabled=False,
            log_group_name="logGroupName",
            log_stream_name="logStreamName"
        ),
        compression_format="compressionFormat",
        encryption_configuration=kinesisfirehose.CfnDeliveryStream.EncryptionConfigurationProperty(
            kms_encryption_config=kinesisfirehose.CfnDeliveryStream.KMSEncryptionConfigProperty(
                awskms_key_arn="awskmsKeyArn"
            ),
            no_encryption_config="noEncryptionConfig"
        ),
        error_output_prefix="errorOutputPrefix",
        prefix="prefix"
    ),
    tags=[CfnTag(
        key="key",
        value="value"
    )]
)