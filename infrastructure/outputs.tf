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