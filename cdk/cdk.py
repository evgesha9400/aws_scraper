#!/usr/bin/env python3

import os

import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_secretsmanager as sm,
    aws_applicationautoscaling as appscaling,
    Stack,
    RemovalPolicy
)
from constructs import Construct


class ScraperStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, f"{id}Vpc", is_default=True)
        security_group = ec2.SecurityGroup.from_lookup_by_name(
            self, f"{id}SecurityGroup", security_group_name="default", vpc=vpc,
        )

        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.all_traffic(),
            "Allow all inbound traffic from all IPv4 addresses",
        )

        db_credentials = rds.Credentials.from_generated_secret(
            "postgres", secret_name=f"{id}RdsSecret"
        )

        sm_secret = sm.Secret.from_secret_name_v2(
            self, f"{id}SecurityManagerSecret", secret_name=db_credentials.secret_name
        )

        db_instance = rds.DatabaseInstance(
            self,
            f"{id}Database",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_15_4),  # type: ignore
            vpc=vpc,
            vpc_subnets={"subnet_type": ec2.SubnetType.PUBLIC},
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.MICRO
            ),
            credentials=db_credentials,
            instance_identifier=f"{id}Database",
            database_name=f"{id}Database",
            allocated_storage=20,
            removal_policy=RemovalPolicy.DESTROY,
            storage_encrypted=True,
            deletion_protection=False,
            availability_zone="eu-west-2a",
            multi_az=False,
            security_groups=[security_group],
        )

        cluster = ecs.Cluster(
            self, f"{id}EcsCluster", cluster_name=f"{id}EcsCluster", vpc=vpc
        )

        task_image_options = ecs_patterns.ScheduledFargateTaskImageOptions(
            image=ecs.ContainerImage.from_asset(
                os.path.join(os.path.dirname(__file__), "../")
            ),
            memory_limit_mib=1024,
            environment={
                "url": "https://www.google.com",
            },
            secrets={
                "database_user": ecs.Secret.from_secrets_manager(sm_secret, "username"),
                "database_password": ecs.Secret.from_secrets_manager(
                    sm_secret, "password"
                ),
                "database_host": ecs.Secret.from_secrets_manager(sm_secret, "host"),
                "database_name": ecs.Secret.from_secrets_manager(sm_secret, "dbname"),
                "database_port": ecs.Secret.from_secrets_manager(sm_secret, "port"),
            },
        )

        scheduled_fargate_task = ecs_patterns.ScheduledFargateTask(
            self,
            f"{id}ScheduledFargateTask",
            cluster=cluster,
            security_groups=[security_group],
            desired_task_count=1,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            scheduled_fargate_task_image_options=task_image_options,
            schedule=appscaling.Schedule.cron(
                hour="12", minute="0"
            ),  # Run at midday every day
            platform_version=ecs.FargatePlatformVersion.LATEST,
        )


app = cdk.App()
env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
)

ScraperStack(app, "Scraper", env=env)
app.synth()
