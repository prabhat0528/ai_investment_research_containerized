#!/usr/bin/env bash
# ==============================================================================
# Script: ec2-bootstrap.sh
# Purpose: Standalone Production Bootstrap for AWS EC2 (Ubuntu 24.04 LTS)
# ==============================================================================
set -e

echo "=========================================================="
echo "Starting EC2 Host Provisioning & Docker Setup..."
echo "=========================================================="

export DEBIAN_FRONTEND=noninteractive

# 1. Update OS packages
apt-get update -y
apt-get upgrade -y
apt-get install -y ca-certificates curl gnupg lsb-release git htop ufw jq unzip

# 2. Configure Firewall (UFW)
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP Frontend
ufw allow 443/tcp   # HTTPS
ufw allow 5005/tcp  # Backend API
ufw allow 3001/tcp  # Preview Frontend
ufw allow 3002/tcp  # Grafana Dashboard
ufw allow 9090/tcp  # Prometheus Server
ufw --force enable

# 3. Install Docker Engine & Docker Compose Plugin
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 4. Configure permissions
usermod -aG docker ubuntu
systemctl enable docker
systemctl start docker

# 5. Create deployment directories
mkdir -p /home/ubuntu/app/monitoring/prometheus
mkdir -p /home/ubuntu/app/monitoring/grafana/provisioning/datasources
mkdir -p /home/ubuntu/app/monitoring/grafana/provisioning/dashboards
chown -R ubuntu:ubuntu /home/ubuntu/app

echo "=========================================================="
echo "EC2 Host Provisioning Completed Successfully!"
echo "Docker Version: $(docker --version)"
echo "Docker Compose Version: $(docker compose version)"
echo "=========================================================="
