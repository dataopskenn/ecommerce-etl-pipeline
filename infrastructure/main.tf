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


resource "aws_db_instance" "d2b" {
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
  password               = "account-password" #random_password.password.result
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