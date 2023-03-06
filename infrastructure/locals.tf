locals {
  config  = yamldecode(file("${path.module}/safe/aws_keys.yml"))
  account_id = data.aws_caller_identity.current.account_id
  tags = {
    created_by = "terraform"
  }
  postgres_identifier = "database-name"
  postgres_db_name = "database-name"
  postgres_user_name = "database-name"
  postgres_password = "${random_password.password.result}"
  postgres_instance_name = "database-name"
  postgres_db_password = "${random_password.password.result}"
  postgres_port = 5432
}

# output "account_id" {
#   value = locals.account_id
# }

#aws_ecr_url = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com"
