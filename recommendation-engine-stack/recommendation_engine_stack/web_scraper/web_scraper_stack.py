from constructs import Construct
from aws_cdk import (
    NestedStack,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_s3_assets as s3_assests,
    aws_lambda as lambda_,
    aws_rds as rds,
)

class WebScraperStack(NestedStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC for EC2 image
        self.vpc = ec2.Vpc(self, 'Scraper_VPC')

        # Create DB for results storage
        scraped_content_db = rds.CfnDBInstance(
            self, 'ScrapedContentDB',
            vpc=self.vpc,
            engine='mysql',
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO
            ),
            # credentials=TODO
        )

        self.scraped_content_db_endpoint = scraped_content_db.instance_endpoint

        # Get Machine Image
        awsLinux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
            cpuType=ec2.AmazonLinuxCpuType.X86_64,
            )

        # Upload scraping script to S3
        scraping_script = s3_assests.Asset(self, 'WebScrapingScript',
            path='scraper.py')

        # Maybe need to install python3?
        init_data = ec2.CloudFormationInit.from_elements(
            ec2.InitFile.from_existing_asset(scraping_script.asset_path, scraping_script),
            ec2.InitPackage('python3-bs4'),
            ec2.InitPackage('selenium'),
            ec2.InitPackage('webdriver-manager'),
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
        lambda_fn = lambda_.Function(self, 'start_scraper_lambda',
            handler='start_scraper.handler',
            code=lambda_.Code.from_asset('lambda'),
            environment={
                'INSTANCE_IP': self.ec2_instance.instance_id,

            })

