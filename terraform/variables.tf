variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-north-1"
}

variable "ssh_cidr" {
  description = "CIDR block allowed to access SSH"
  type        = string
  default     = "88.238.11.235/32"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "cloudops-lab"
}
