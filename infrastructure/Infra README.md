# Terraform Infrastructure Setup


## backend.tf

This file contains the configuration for our Terraform Organization. This will tell/show terraform where to push/store the workflow to, pending further instructions. From the organization's workspace, Version Control, GitHub Actions and merge GitHub branches (if they meet any form of test we could set up) can be set up. In other words, deployment can be managed directly from `Terraform Cloud`.

The format for setting this up is:

```hcl

terraform {
  cloud {
    organization = "organization's name"

    workspaces {
      name = "workspace/db_name"
    }
  }
}

```


## data.tf

Contains parameters collected directly from our AWS instances, some to be use for a docker container, others for our RDS instance. The parameters needed are as follows;

```hcl

data "aws_caller_identity" "current" {}

data "aws_ecr_authorization_token" "token" {}

data "aws_vpc" "secure-vpc" {
  default = true
}

```


## locals.tf

Contains locally initialized parameters for the RDS instance. The `main.tf` file will pick these initializations from here and insert them into the main infrastructure code. These parameters are;

```hcl

locals {
  account_id = data.aws_caller_identity.current.account_id
  tags = {
    created_by = "terraform"
  }
  postgres_identifier = "identifier_name"
  postgres_db_name = "db_name"
  postgres_user_name = "postgres_username/db_name"
  posotgres_password = "${random_password.password.result}"
  postgres_instance_name = "postgres_instance name"
  postgres_db_password = "your_password" #"${random_password.password.result}"
  postgres_port = 5432
}

```


## outputs.tf

Contains all the parameters needed to connect with `PgAdmin4` and more. These parameters will be printed to Terminal console and therefore needs to be protected. The reason for the output is to save them in terraform cloud, from where they can be copied and used for other needed purposes.

- `random_password`: To create a random password that can be used for docker container
- `vpc_id`: The id to the virtual private cloud space, needed to help docker locate the RDS instance
- `db_endpoint`: Host name for our RDS instance, needed both for Python, Docker and PgAdmin4
- `db_name`: The name of our RDS database instance, this is also a parameter needed for Python, Docker and PgAdmin4
- `port`: The port number, usually 5432, a parameter needed for Python, Docker and PgAdmin4
- `ecr_id`, `ecr_registry_id`, `ecr_repository_url`: all parameters needed for Docker, and Terraform

```hcl

output "random_password" {
    value = random_password.password
    sensitive = true
}

output "vpc_id" {
    value = aws_security_group.secure-one.id
}

output "db_endpoint" {
    value = aws_db_instance.database-name.endpoint
}

output "db_name" {
    value = aws_db_instance.database-name.db_name
}

output "port" {
    value = aws_db_instance.database-name.port
}

output "ecr_id" {
    value = aws_ecr_repository.repository.id
}

output "ecr_registry_id" {
    value = aws_ecr_repository.repository.registry_id
}

output "ecr_repository_url" {
    value = aws_ecr_repository.repository.repository_url
}

```


## provider.tf

Ideally, this should contain the configuartions for all the providers used for this project, but those have already been configured in the `main.tf` file, duplicatin them will result in error when running `terraform apply`. This file is left empty for this project.


## variables.tf

Contains all the variables declared for this project, so that they can be concealed from the main IaC file. The variables for this projects are;

- `region`: the AWS availability zone closest to this geographic location
- `access_key`: AWS account access key
- `secret_key`: AWS account secret key
- `repository_list`: Proposed repository names for our backend and worker jobs, especially for pushing docker images to terraform cloud
- `repositry`: the single repository we eventually used

```hcl

variable "region" {
  description = "AWS region to create resources in"
  type        = string
  default     = "host.avail-zone"
}

variable "access_key" {
  description = "aws access key value"
  type = string
  default = "aws-access-key"
}

variable "secret_key" {
  description = "aws secret key value"
  type = string
  default = "aws-secret-key"
}

#variable "repository_list" {
#  description = "List of repository names"
#  type        = list(any)
#  default     = ["backend", "worker"]
#}

variable "repository" {
  description = "List of repository names"
  type        = string
  default     = "backend"
}

```

## main.tf

The main terraform IaC file, where our AWS, Terraform, and Docker infrastructure are built, integrated from the different `.tf` files and applied. This file contains all the resources needed to create the "fully managed" engineering infrastructure for this project. The infrastructure can be built/written, initialized, planned, executed, and destroyed from from this file.

```hcl

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.39.0"
    }

    hcp = {
      source  = "hashicorp/hcp"
      version = "0.48.0"
    }
  }
}


provider "aws" {
  region     = var.region
  access_key = var.access_key
  secret_key = var.secret_key
}


resource "random_password" "password" {
  length           = 10
  special          = false
  override_special = "_%@"
}


resource "aws_security_group" "secure-one" {
  vpc_id      = data.aws_vpc.secure-vpc.id
  name        = "first_secure"
  description = "Allow all inbound for Postgres"

  ingress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    description = "aws"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    description = "PostgreSQL"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_db_instance" "database-name" {
  identifier             = local.postgres_identifier
  db_name                = local.postgres_db_name
  instance_class         = "db.m5.large"
  allocated_storage      = 200
  engine                 = "postgres"
  engine_version         = "14"
  skip_final_snapshot    = true
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.secure-one.id]
  username               = local.postgres_user_name
  password               = "password" #random_password.password.result
  port                   = 5432
}


resource "aws_ecr_repository" "repository" {
  #for_each = toset(var.repository_list)
  #name     = each.key
  name                 = var.repository
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

```

In the `aws_security_group` resource, three `ingress` parameters were declared to make sure that the RDB instance can accept input or queries both from `localhost` (port "0"), `aws ssh` (port "22"), and `postgres or PgAdmin4` (port "5432") and from any IP-Address (cidr block ["0.0.0.0/0"])