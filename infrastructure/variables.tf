variable "region" {
  description = "AWS region to create resources in"
  type        = string
  default     = "avail-zone"
}

variable "access_key" {
  description = "aws access key value"
  type = string
  default = locals.config.access_key
}

variable "secret_key" {
  description = "aws secret key value"
  type = string
  default = locals.config.secret_key 
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