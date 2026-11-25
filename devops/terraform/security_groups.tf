# Security Group Hardening for AI Investment Research Suite
resource "aws_security_group" "app_sg" {
  name        = "ai-investment-sg-${var.environment}"
  description = "Controls ingress and egress traffic for AI Investment Suite and Telemetry"
  vpc_id      = aws_vpc.main.id

  # SSH remote administration
  ingress {
    description = "SSH administrative access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  # Production Web Frontend (Nginx)
  ingress {
    description = "HTTP Public Web Traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSL Secured Traffic
  ingress {
    description = "HTTPS Secured Web Traffic"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Production Backend API Service
  ingress {
    description = "Backend REST API service"
    from_port   = 5005
    to_port     = 5005
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Frontend alternative dev/preview port
  ingress {
    description = "Frontend preview port"
    from_port   = 3001
    to_port     = 3001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Grafana Telemetry Dashboard
  ingress {
    description = "Grafana Observability Dashboard"
    from_port   = 3002
    to_port     = 3002
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Prometheus Metrics Scraper UI
  ingress {
    description = "Prometheus Server UI"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  # Outbound connectivity to Docker Hub, GitHub, and external financial APIs
  egress {
    description = "Full outbound internet access for packages and container images"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ai-investment-sg-${var.environment}"
  }
}
