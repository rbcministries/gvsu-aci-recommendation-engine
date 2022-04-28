import boto3
import os
import json

ENDPOINT_NAME = os.environ['endpoint_name']
CONTENT_TYPE = os.environ['content_type']

def handler(event, context):
    data = json.loads(json.dumps(event))
    payload = data['data']
    
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType=CONTENT_TYPE,
                                       Body=payload)
                                       
    # Need return format from Tom, which is probably dependant on Joe for now.
    result = json.loads(response['Body'].read().decode())
    
    return result