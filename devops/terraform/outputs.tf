output "vpc_id" {
  description = "The ID of the custom VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "The ID of the public subnet"
  value       = aws_subnet.public.id
}

output "ec2_instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

output "ec2_public_ip" {
  description = "Public IP address of the EC2 server (for SSH, Web UI, and Grafana)"
  value       = aws_instance.app_server.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS hostname of the EC2 server"
  value       = aws_instance.app_server.public_dns
}

output "s3_bucket_name" {
  description = "Name of the S3 storage bucket for investment reports"
  value       = aws_s3_bucket.report_storage.bucket
}

output "s3_bucket_arn" {
  description = "ARN of the S3 storage bucket"
  value       = aws_s3_bucket.report_storage.arn
}

output "ssh_command" {
  description = "Ready-to-use SSH connection command"
  value       = "ssh -i ${var.ssh_key_name}.pem ubuntu@${aws_instance.app_server.public_ip}"
}

output "web_url" {
  description = "Public Frontend Web Application URL"
  value       = "http://${aws_instance.app_server.public_ip}"
}

output "grafana_url" {
  description = "Grafana Observability Dashboard URL"
  value       = "http://${aws_instance.app_server.public_ip}:3002"
}

output "backend_api_url" {
  description = "Backend REST API Base URL"
  value       = "http://${aws_instance.app_server.public_ip}:5005"
}
