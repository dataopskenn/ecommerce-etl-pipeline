#terraform {
#  required_providers {
#    aws = {
#      source  = "hashicorp/aws"
#      version = "3.47.0"
#    }
#  }
#}

provider "aws" {
  region     = "eu-west-2"
  access_key = "aws_access_key"
  secret_key = "aws_secret_key"
}

data "aws_vpc" "secure-vpc" {
  default = true
}

resource "random_password" "password" {
  length           = 20
  special          = false
  override_special = "_%@"
}

resource "aws_security_group" "secure-one" {
  vpc_id      = data.aws_vpc.secure-vpc.id
  name        = "used_999"
  description = "Allow all inbound for Postgres"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "user9999" {
  identifier             = "user9999"
  db_name                = "used_999"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "14"
  skip_final_snapshot    = true
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.secure-one.id]
  username               = "user9999"
  password               = "random_password.password.result}"
}
