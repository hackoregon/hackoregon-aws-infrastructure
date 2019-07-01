# HackOregon 2017-2019 - Infrastructure

A Set of YAML templates for deploying the HackOregon infrastructure on [Amazon EC2 Container Service (Amazon ECS)](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html) with [AWS CloudFormation](https://aws.amazon.com/cloudformation/). Based on the AWSLabs [EC2 Container Service Reference Architecture](https://github.com/awslabs/ecs-refarch-cloudformation).

## Related Repositories

* [Example Django Docker with CI/CD](https://github.com/hackoregon/backend-service-pattern)
* [Example Nginix Docker Endpoint Catalog Service with CI/CD](https://github.com/hackoregon/endpoint-service-catalog)

## Overview

![infrastructure-overview](images/architecture-overview.png)

The repository consists of a set of nested templates that deploy the following:

 - A tiered [VPC](http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Introduction.html) with public and private subnets, spanning an AWS region.
 - A highly available ECS cluster deployed across two [Availability Zones](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html) in an [Auto Scaling](https://aws.amazon.com/autoscaling/) group.
 - A pair of [NAT gateways](http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/vpc-nat-gateway.html) (one in each zone) to handle outbound traffic.
 - A variety of microservice and web front-end containers deployed as [ECS services](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html).
 - An [Application Load Balancer (ALB)](https://aws.amazon.com/elasticloadbalancing/applicationloadbalancer/) to the public subnets to handle inbound traffic to the load-balanced container duplicates.
 - ALB path-based routes for each ECS service to route the inbound traffic to the correct service.
 - Centralized container logging with [Amazon CloudWatch Logs](http://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html).

#### Infrastructure-as-Code

This set of templates can be used to create near-identical copies of the same stack (or to use as a foundation to start a new stack).

Master templates correspond to the following deployed clusters in Hack Oregon:
1. `master.yaml` - the historical "hacko-integration" cluster that has been used as test/staging/production since Hack Oregon's 2017 project season.
2. (Coming soon) `master-staging.yaml` - a dedicated staging environment for all 2017+ Hack Oregon projects.  Looser access to developers, deploys from `develop` branch or equivalent in each project, limited resources to keep costs down.
3. (Coming soon) `master-production.yaml` - a dedicated production environment for all 2017+ Hack Oregon projects.  Restricted access to developers, only deploys from `master` branch in each project, production-grade resource allocation (greater number of load-balanced tasks, higher Cpu and Memory resource allocation).

#### Updating and Rollback

This CloudFormation stack not only handles the initial deployment of the HackOregon infrastructure and environments, but it can also manage the whole lifecycle, including future updates. During updates, you have fine-grained control and visibility over how changes are applied, using functionality such as [change sets](https://aws.amazon.com/blogs/aws/new-change-sets-for-aws-cloudformation/), [rolling update policies](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html) and [stack policies](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/protect-stack-resources.html).

## Template details

The templates below are included in this repository and reference architecture:

| Template | Description |
| --- | --- |
| [master.yaml](master.yaml) | This is the master template - deploy it to CloudFormation and it includes all of the others automatically. |
| [infrastructure/vpc.yaml](infrastructure/vpc.yaml) | This template deploys a VPC with a pair of public and private subnets spread across two Availability Zones. It deploys an [Internet gateway](http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Internet_Gateway.html), with a default route on the public subnets. It deploys a pair of NAT gateways (one in each zone), and default routes for them in the private subnets. |
| [infrastructure/security-groups.yaml](infrastructure/security-groups.yaml) | This template contains the [security groups](http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_SecurityGroups.html) required by the entire stack. They are created in a separate nested template, so that they can be referenced by all of the other nested templates. |
| [infrastructure/load-balancers.yaml](infrastructure/load-balancers.yaml) | This template deploys an ALB to the public subnets, which exposes the various ECS services. It is created in in a separate nested template, so that it can be referenced by all of the other nested templates and so that the various ECS services can register with it. |
| [infrastructure/ecs-cluster.yaml](infrastructure/ecs-cluster.yaml) | This template deploys an ECS cluster to the private subnets using an Auto Scaling group. |
| [infrastructure/rds.yaml](infrastructure/rds.yaml) | This is an example of how to deploy RDS postgres service on AWS.  We can do a Single or Multiple AZ deploy.|
| [infrastructure/ec2-instance.yaml](infrastructure/ec2-instance.yaml) | Example of how to deploy the ec2 instances into the private subnet. The [master.yaml](masteryaml) template has examples for a bastion host and postgres db servers based on hackoregon db AMIs.|
| [services/homelesss-service/service.yaml](infrastructure/homeless-service/service.yaml) | This is an example of the long-running Django DRF ECS service that serves a JSON API for the homelessness project. For the full source for the service, see [HackOregon Back End Service Pattern](https://github.com/hackoregon/backend-service-pattern).|
| [services/endpoint-service/service.yaml](https://github.com/hackoregon/endpoint-service-catalog) | This is an example of a long-running Nginx ECS service that provides a static catalog of available services via the load-balanced URL.  For the full source for this service, see [HackOregon Endpoint Service Catalog](https://github.com/hackoregon/endpoint-service-catalog). |

After the CloudFormation templates have been deployed, the [stack outputs](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html) contain a link to the load-balanced URLs for each of the deployed microservices.

![stack-outputs](images/stack-outputs.png)

## How do I...?

### How to Deploy

Stack is setup to launch stack in the us-west-2 (Oregon) region in your account:

- from the root of your copy of the repo, run `aws s3 cp . s3://hacko-infrastructure-cfn --recursive --exclude ".git/*"`
- copy the URL for the `master.yaml` (or other master-*.yaml template) file from S3
- go to AWS CloudFormation - if creating new stack (e.g. for testing), choose "create stack"; if updating an existing stack, select that stack then click the *Update* button

#### Security requirements

The account of the AWS user who initially creates the stack requires many privileges in AWS, including:

* IAM Role creation
* IAM Policy creation

Subsequent incremental Updates to an existing stack can sometimes be performed by AWS users with less privileges, depending on which stack objects are being created, updated or deleted.

### Customize the templates

1. [Fork](https://github.com/hackoregon/hackoregon-aws-infrastructure#fork-destination-box) this GitHub repository.
2. Clone the forked GitHub repository to your local machine.
3. Modify the templates.
4. Upload them to an Amazon S3 bucket of your choice.
5. Either create a new CloudFormation stack by deploying the master.yaml template, or update your existing stack with your version of the templates.

### Create a new service

1. Push your container to a registry somewhere (e.g., [Docker Hub](https://hub.docker.com/), [Amazon ECR](https://aws.amazon.com/ecr/)).
2. Copy one of the existing service templates in [services/*](/services).
3. Update the `ContainerName` and `Image` parameters to point to your container image instead of the example container.
4. Increment the `ListenerRule` priority number (no two services can have the same priority number - this is used to order the ALB path based routing rules).
5. Duplicate one of the existing service definitions in [master.yaml](master.yaml) and point it at your new service template. Specify the HTTP `Path` at which you want the service exposed.
6. Deploy the templates as a new stack, or as an update to an existing stack.

### Setup centralized container logging

By default, the containers in your ECS tasks/services are already configured to send log information to CloudWatch Logs and retain them for 365 days. Within each service's template (in [services/*](services/)), a LogGroup is created that is named after the CloudFormation stack. All container logs are sent to that CloudWatch Logs log group.

You can view the logs by looking in your [CloudWatch Logs console](https://console.aws.amazon.com/cloudwatch/home?#logs:) (make sure you are in the correct AWS region).

ECS also supports other logging drivers, including `syslog`, `journald`, `splunk`, `gelf`, `json-file`, and `fluentd`. To configure those instead, adjust the service template to use the alternative `LogDriver`. You can also adjust the log retention period from the default 365 days by tweaking the `RetentionInDays` parameter.

For more information, see the [LogConfiguration](http://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_LogConfiguration.html) API operation.

### Change the ECS host instance type

This is specified in the [master.yaml](master.yaml) template.

By default, [t2.large](https://aws.amazon.com/ec2/instance-types/) instances are used, but you can change this by modifying the following section:

```
ECS:
  Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: ...
      Parameters:
        ...
        InstanceType: t2.large
        InstanceCount: 4
        ...
```

### Adjust the Auto Scaling parameters for ECS hosts and services

The Auto Scaling group scaling policy provided by default launches and maintains a cluster of 2 ECS hosts distributed across two Availability Zones (min: 2, max: 2, desired: 2).

It is ***not*** set up to scale automatically based on any policies (CPU, network, time of day, etc.).

If you would like to configure policy or time-based automatic scaling, you can add the [ScalingPolicy](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html) property to the AutoScalingGroup deployed in [infrastructure/ecs-cluster.yaml](infrastructure/ecs-cluster.yaml#L69).

As well as configuring Auto Scaling for the ECS hosts (your pool of compute), you can also configure scaling each individual ECS service. This can be useful if you want to run more instances of each container/task depending on the load or time of day (or a custom CloudWatch metric). To do this, you need to create [AWS::ApplicationAutoScaling::ScalingPolicy](http://docs.aws.amazon.com/pt_br/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html) within your service template.

### Deploy multiple environments (e.g., dev, test, pre-production)

Deploy another CloudFormation stack from the same set of templates to create a new environment. The stack name provided when deploying the stack is prefixed to all taggable resources (e.g. EC2 instances, VPCs, etc.) so you can distinguish the different environment resources in the AWS Management Console.

To distinguish between e.g. staging and production configurations, you will need to author multiple `master.yaml` files, each with the specific parameter values (e.g. `Host` or `PublicAlbAcmCertificate`) that address e.g. the specific DNS addresses to reach each stack's otherwise-nearly-identical resources.

### Change the VPC or subnet IP ranges

This set of templates deploys the following network design:

| Item | CIDR Range | Usable IPs | Description |
| --- | --- | --- | --- |
| VPC | 10.180.0.0/16 | 65,536 | The whole range used for the VPC and all subnets |
| Public Subnet | 10.180.8.0/21 | 2,041 | The public subnet in the first Availability Zone |
| Public Subnet | 10.180.16.0/21 | 2,041 | The public subnet in the second Availability Zone |
| Private Subnet | 10.180.24.0/21 | 2,041 | The private subnet in the first Availability Zone |
| Private Subnet | 10.180.32.0/21 | 2,041 | The private subnet in the second Availability Zone |

You can adjust the CIDR ranges used in this section of the [master.yaml](master.yaml) template:

```
VPC:
  Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub ${TemplateLocation}/infrastructure/vpc.yaml
      Parameters:
        EnvironmentName:    !Ref AWS::StackName
        VpcCIDR:            10.180.0.0/16
        PublicSubnet1CIDR:  10.180.8.0/21
        PublicSubnet2CIDR:  10.180.16.0/21
        PrivateSubnet1CIDR: 10.180.24.0/21
        PrivateSubnet2CIDR: 10.180.32.0/21
```

### Update an ECS service to a new Docker image version

ECS has the ability to perform rolling upgrades to your ECS services to minimize downtime during deployments. For more information, see [Updating a Service](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/update-service.html).

To update one of your services to a new version, adjust the `Image` parameter in the service template (in [services/*](services/) to point to the new version of your container image. For example, if `1.0.0` was currently deployed and you wanted to update to `1.1.0`, you could update it as follows:

```
TaskDefinition:
  Type: AWS::ECS::TaskDefinition
  Properties:
    ContainerDefinitions:
      - Name: your-container
        Image: registry.example.com/your-container:1.1.0
```

After you've updated the template, update the deployed CloudFormation stack; CloudFormation and ECS handle the rest.

To adjust the rollout parameters (min/max number of tasks/containers to keep in service at any time), you need to configure `DeploymentConfiguration` for the ECS service.

For example:

```
Service:
  Type: AWS::ECS::Service
    Properties:
      ...
      DesiredCount: 4
      DeploymentConfiguration:
        MaximumPercent: 200
        MinimumHealthyPercent: 50
```

## Contributing

Please [create a new GitHub issue](https://github.com/hackoregon/hackoregon-aws-infrastructure/issues/new) for any feature requests, bugs, or documentation improvements.

Where possible, please also [submit a pull request](https://help.github.com/articles/creating-a-pull-request-from-a-fork/) for the change.

## License

Copyright 2011-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

[http://aws.amazon.com/apache2.0/](http://aws.amazon.com/apache2.0/)

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
