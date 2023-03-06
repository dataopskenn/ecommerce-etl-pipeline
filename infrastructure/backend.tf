#terraform {
#  required_providers {
#    docker = {
#      source  = "kreuzwerker/docker"
#      version = "2.15.0"
#    }
#  }
#  backend "remote" {
#    hostname     = "app.terraform.io"
#    organization = "dataopskenn"

#    workspaces {
#      prefix = "d2b"
#    }
#  }
#}

terraform {
  cloud {
    organization = "terraform_organization"

    workspaces {
      name = "db_name"
    }
  }
}