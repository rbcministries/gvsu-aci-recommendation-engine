from constructs import Construct
from aws_cdk import (
    Stack,
    aws_gluw as glue,
    aws_lakeformation as lakeformation
)

class DatalakeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a crawler
        cfn_crawler = glue.CfnCrawler(self, "MyCfnCrawler",
            role="role",
            targets=glue.CfnCrawler.TargetsProperty(
                catalog_targets=[glue.CfnCrawler.CatalogTargetProperty(
                    database_name="databaseName",
                    tables=["tables"]
                )],
                dynamo_db_targets=[glue.CfnCrawler.DynamoDBTargetProperty(
                    path="path"
                )],
                jdbc_targets=[glue.CfnCrawler.JdbcTargetProperty(
                    connection_name="connectionName",
                    exclusions=["exclusions"],
                    path="path"
                )],
                mongo_db_targets=[glue.CfnCrawler.MongoDBTargetProperty(
                    connection_name="connectionName",
                    path="path"
                )],
                s3_targets=[glue.CfnCrawler.S3TargetProperty(
                    connection_name="connectionName",
                    dlq_event_queue_arn="dlqEventQueueArn",
                    event_queue_arn="eventQueueArn",
                    exclusions=["exclusions"],
                    path="path",
                    sample_size=123
                )]
            ),

            # the properties below are optional
            # classifiers=["classifiers"],
            # configuration="configuration",
            # crawler_security_configuration="crawlerSecurityConfiguration",
            # database_name="databaseName",
            # description="description",
            # name="name",
            # recrawl_policy=glue.CfnCrawler.RecrawlPolicyProperty(
            #     recrawl_behavior="recrawlBehavior"
            # ),
            # schedule=glue.CfnCrawler.ScheduleProperty(
            #     schedule_expression="scheduleExpression"
            # ),
            # schema_change_policy=glue.CfnCrawler.SchemaChangePolicyProperty(
            #     delete_behavior="deleteBehavior",
            #     update_behavior="updateBehavior"
            # ),
            # table_prefix="tablePrefix",
            # tags=tags
        )

        # Manages the data lake settings for your account
        cfn_data_lake_settings = lakeformation.CfnDataLakeSettings(self, "MyCfnDataLakeSettings",
        admins=[lakeformation.CfnDataLakeSettings.DataLakePrincipalProperty(
            data_lake_principal_identifier = "dataLakePrincipalIdentifier"
        )],
        trusted_resource_owners = ["trustedResourceOwners"]
        )

        # Represents the data (Amazon S3 buckets and folders) that is being registered with AWS Lake Formation
        cfn_resource = lakeformation.CfnResource(self, "MyCfnResource",
        resource_arn="resourceArn",
        use_service_linked_role=False,
        # the properties below are optional
        # role_arn="roleArn"
        )

        # The AWS::LakeFormation::Permissions resource represents the permissions that a principal has on an
        # AWS Glue Data Catalog resource (such as AWS Glue database or AWS Glue tables). When you upload
        # a permissions stack, the permissions are granted to the principal and when you remove the stack,
        # the permissions are revoked from the principal.
        cfn_permissions = lakeformation.CfnPermissions(self, "MyCfnPermissions",
            data_lake_principal=lakeformation.CfnPermissions.DataLakePrincipalProperty(
            data_lake_principal_identifier="dataLakePrincipalIdentifier"
            ),
            resource=lakeformation.CfnPermissions.ResourceProperty(
                database_resource=lakeformation.CfnPermissions.DatabaseResourceProperty(
                    catalog_id="catalogId",
                    name="name"
                ),
                data_location_resource=lakeformation.CfnPermissions.DataLocationResourceProperty(
                    catalog_id="catalogId",
                    s3_resource="s3Resource"
                ),
                table_resource=lakeformation.CfnPermissions.TableResourceProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    name="name",
                    table_wildcard=lakeformation.CfnPermissions.TableWildcardProperty()
                ),
                table_with_columns_resource=lakeformation.CfnPermissions.TableWithColumnsResourceProperty(
                    catalog_id="catalogId",
                    column_names=["columnNames"],
                    column_wildcard=lakeformation.CfnPermissions.ColumnWildcardProperty(
                        excluded_column_names=["excludedColumnNames"]
                    ),
                    database_name="databaseName",
                    name="name"
                )
            ),
        # the properties below are optional
        # permissions=["permissions"],
        # permissions_with_grant_option=["permissionsWithGrantOption"]
        )