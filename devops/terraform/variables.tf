variable "aws_region" {
  description = "AWS region for provisioning resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "vpc_cidr" {
  description = "Base CIDR block for the custom VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public application subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "Target availability zone"
  type        = string
  default     = "us-east-1a"
}

variable "instance_type" {
  description = "EC2 Instance size (t2.micro for Free Tier, t3.small/medium for production)"
  type        = string
  default     = "t3.small"
}

variable "ssh_key_name" {
  description = "Name of existing AWS EC2 Key Pair for SSH remote access"
  type        = string
  default     = "ai-investment-key"
}

variable "dockerhub_user" {
  description = "Docker Hub account identifier for pulling container images"
  type        = string
  default     = "prabhatrai05"
}

variable "allowed_ssh_cidr" {
  description = "IP CIDR permitted to SSH into the EC2 instance (recommend restricting to your IP)"
  type        = string
  default     = "0.0.0.0/0"
}
