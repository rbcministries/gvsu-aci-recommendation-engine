from constructs import Construct
from aws_cdk import (
    NestedStack,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_s3_assets as s3_assests,
    aws_lambda as lambda_,
)

class WebScraperStack(NestedStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC for EC2 image
        self.vpc = ec2.Vpc(self, 'Scraper_VPC')

        # Get Machine Image
        awsLinux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
            cpuType=ec2.AmazonLinuxCpuType.X86_64,
            )

        # Upload scraping script to S3
        scraping_script = s3_assests.Asset(self, 'Web_Scraping_Script',
            path='scraper.py')

        init_data = ec2.CloudFormationInit.from_elements(
            ec2.InitFile.from_existing_asset('scraper.py', scraping_script)
        )

        self.ec2_instance = ec2.Instance(self, 'WebScraping',
            vpc=self.vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.STANDARD3, 
                ec2.InstanceSize.SMALL),
            machine_image=awsLinux,
            init=init_data
            )

        # For now we will just load the script onto the server]
        # Work out how to start/stop later
        # lambda_fn = lambda_.Function(self, 'start_scraper_lambda',
        #     handler='lambda_handler.handler',
        #     code=lambda_.Code.from_asset('lambda'))

