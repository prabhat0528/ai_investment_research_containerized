# Lookup latest official Ubuntu 24.04 LTS AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Production EC2 Instance
resource "aws_instance" "app_server" {
  ami                  = data.aws_ami.ubuntu.id
  instance_type        = var.instance_type
  subnet_id            = aws_subnet.public.id
  key_name             = var.ssh_key_name
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  vpc_security_group_ids = [
    aws_security_group.app_sg.id
  ]

  root_block_device {
    volume_size           = 25
    volume_type           = "gp3"
    delete_on_termination = true
    encrypted             = true

    tags = {
      Name = "ai-investment-root-volume"
    }
  }

  # User Data bootstrap script: Installs Docker, Docker Compose, Git, and Prepares Directory
  user_data = <<-EOF
              #!/bin/bash
              set -e

              # Update system packages
              apt-get update -y
              apt-get install -y ca-certificates curl gnupg lsb-release git htop ufw

              # Install Docker Engine
              mkdir -p /etc/apt/keyrings
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
              echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

              apt-get update -y
              apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

              # Enable Docker service and grant permissions to ubuntu user
              usermod -aG docker ubuntu
              systemctl enable docker
              systemctl start docker

              # Create application directory structure
              mkdir -p /home/ubuntu/app/monitoring/prometheus
              mkdir -p /home/ubuntu/app/monitoring/grafana/provisioning/datasources
              mkdir -p /home/ubuntu/app/monitoring/grafana/provisioning/dashboards
              chown -R ubuntu:ubuntu /home/ubuntu/app

              echo "EC2 Provisioning and Docker Bootstrap completed successfully." > /var/log/bootstrap.log
              EOF

  tags = {
    Name = "ai-investment-app-host-${var.environment}"
    Role = "Application-And-Telemetry-Host"
  }
}
