import aws_cdk.aws_cloudwatch
import aws_cdk.aws_iam as iam
import json
from constructs import Construct
from aws_cdk import (
    Duration,
    NestedStack,
    aws_cloudwatch as cw,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
    aws_sns_subscriptions as sns_subscriptions,
    aws_apigateway as api_gw
)

import boto3
from datetime import datetime
AWS_REGION = 'us-east-1'
cloudwatch = boto3.client('cloudwatch', region_name=AWS_REGION)
iam = boto3.client('iam')


class CloudWatchStack(NestedStack):

    def __init__(self, scope: Construct, id: str, api: api_gw.RestApi, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        topic = sns.Topic(self, id="CW_Topic", display_name="CloudWatch Topic")

        topic.add_subscription(sns_subscriptions.EmailSubscription("joe.fahnestock@odb.org"))
        topic.add_subscription(sns_subscriptions.EmailSubscription("dykemami@mail.gvsu.edu"))
        topic.add_subscription(sns_subscriptions.EmailSubscription("linderem@mail.gvsu.edu"))
        topic.add_subscription(sns_subscriptions.EmailSubscription("johnsjm1@mail.gvsu.edu"))
        topic.add_subscription(sns_subscriptions.EmailSubscription("lobbestt@mail.gvsu.edu"))

        # Alarm for number of client-side API errors
        api_client_error_alarm = cw.Alarm(
            self, 
            id="api_client_errors_alarm",
            alarm_description="Sends an alarm when too many client errors have occurred",
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=10,
            evaluation_periods=1,
            metric=api.metric_client_error(
                label="api_client_errors",
                period=Duration.hours(1)
            )
        )

        api_client_error_alarm.add_alarm_action(cw_actions.SnsAction(topic))

        # Alarm for number of client-side API errors
        api_server_error_alarm = cw.Alarm(
            self, 
            id="api_server_errors_alarm",
            alarm_description="Sends an alarm when too many server errors have occurred",
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=10,
            evaluation_periods=1,
            metric=api.metric_server_error(
                label="api_server_errors",
                period=Duration.hours(1)
            )
        )

        api_server_error_alarm.add_alarm_action(cw_actions.SnsAction(topic))

        # Alarm for numbers of requests (AKA cost)
        api_count_alarm = cw.Alarm(
            self, 
            id="api_count_alarm",
            alarm_description="Sends an alarm when too requests have occurred",
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=100000,
            evaluation_periods=24*7,
            metric=api.metric_server_error(
                label="api_server_errors",
                period=Duration.hours(1)
            )
        )

        api_count_alarm.add_alarm_action(cw_actions.SnsAction(topic))

        # creating policy with necessary trust perms for firehose -- will be used to set up metric stream
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "firehose:PutRecord",
                        "firehose:PutRecordBatch"
                    ],
                    "Effect": "Allow",
                    "Resource": "arn:aws:firehose:region:account-id:deliverystream/*"
                },
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "streams.metrics.cloudwatch.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        iam.create_policy(
            PolicyName='cloudwatch-metric-policy',
            PolicyDocument=json.dumps(policy)
        )

        # need to crete iam role & get arn, get firehose arn
        cfn_metric_stream = cloudwatch.CfnMetricStream(self, "DataLakeMetricStream",
                                                       firehose_arn="firehoseArn",
                                                       output_format="json",
                                                       role_arn="roleArn"
                                                       )

        # Eventually need to do other services such as SageMaker

        """need to finish looking into this -- might be the wrong approach"""
        # sm_metric = client.get_metric_data(
        #     MetricDataQueries=[
        #         {
        #             'Id': 'sm1',
        #             'MetricStat': {
        #                 'Metric': {
        #                     'Namespace': 'AWS/SageMaker',
        #                     'MetricName': 'Invocations',
        #                     'Dimensions': [
        #                         {
        #                             'Name': 'EndpointName',
        #                             'Value': 'users-hcl-2'
        #                         },
        #                         {
        #                             'Name': 'VariantName',
        #                             'Value': 'AllTraffic'
        #                         }
        #                     ],
        #                     'Period': 300,
        #                     'Stat': 'Sum',
        #                     'Unit': 'None'
        #                 }
        #             }
        #         },
        #     ],
        #     StartTime=datetime(2022, 3, 20),
        #     EndTime=datetime(2022, 4, 9)
        # )
        #
