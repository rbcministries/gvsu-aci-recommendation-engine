from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event_source,
    Aws, Stack
)

# https://github.com/aws-samples/aws-cdk-examples/blob/master/python/api-cors-lambda/app.py
class ApiStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #Create an API GW Rest API
        base_api = apigw.RestApi(self, 'ApiGW', rest_api_name='RecommendationAPI')

        #Create a resource named "example" on the base API
        api_resource = base_api.root.add_resource('example')

        # Sample code for initial setup of API - waiting for recommendation engine to be setup
        # to connect to that. Will probably be through a Lambda function would be my guess.
        example_lambda = _lambda.Function(self, "ApiSampleLambda",
                                         handler='lambda_handler.handler',
                                         code=_lambda.Code.from_asset('lambda'))

        example_entity_lambda_integration = apigw.LambdaIntegration(
            example_lambda,
            proxy=False,
            integration_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Origin': "'*'",
                }
            }]
        )

        api_resource.add_method(
            'GET', example_entity_lambda_integration,
            method_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Origin': True,
                }
            }]
        )

        '''
        Stuff for integration with SageMaker/Recommendation engine later

        #Create the API GW service role with permissions to call SageMaker if needed.
        rest_api_role = iam.Role(
            self,
            "RestAPIRole",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess")] # Need to figure out the right permissions
        )
        '''