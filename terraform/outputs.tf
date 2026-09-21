output "vpc_id" {
  description = "ID of the default VPC"
  value       = data.aws_vpc.default.id
}

output "security_group_id" {
  description = "ID of the CloudOps security group"
  value       = aws_security_group.cloudops.id
}

output "ec2_instance_id" {
  description = "ID of the CloudOps EC2 instance"
  value       = aws_instance.cloudops.id
}

output "ec2_private_ip" {
  description = "Private IP of the CloudOps EC2 instance"
  value       = aws_instance.cloudops.private_ip
}
