import json
import boto3
import paramiko
import os

instance_ip = os.environ['INSTANCE_IP']
bucket_name = os.environ['BUCKET_NAME']
pem_name = os.environ['PEM_NAME']
pem_path = '/key/scraper.pem'

'''
Ideas for improving:
Figure out if script is already running
Connect/start a different way so don't need a key/pair
'''

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    s3_client = boto3.client('s3')
    
    # downloading pem file from S3 
    s3_client.download_file(bucket_name, pem_name, pem_path)

    # reading pem file and creating key object
    key = paramiko.RSAKey.from_private_key_file(pem_path)
    # an instance of the Paramiko.SSHClient
    ssh_client = paramiko.SSHClient()
    # setting policy to connect to unknown host
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect using ec2 instance ID if requires
    ssh_client.connect(hostname=instance_ip, username="start_lambda", pkey=key)

    # command list
    commands = [
        "python start_scraper.py",
    ]

    # executing list of commands within server
    print("Starting execution")
    for command in commands:
        print("Executing command: " + command)
        stdin , stdout, stderr = ssh_client.exec_command(command)
        print(stdout.read())
        print(stderr.read())
    
    print("finished execution")

    return {
        'statusCode': 200,
        'body': json.dumps('Execution Completed')
    }