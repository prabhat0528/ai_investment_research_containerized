#!/usr/bin/env bash
# ==============================================================================
# Script: deploy-ec2.sh
# Purpose: Zero-Downtime Deployment Trigger over SSH
# Usage: ./deploy-ec2.sh <EC2_PUBLIC_IP> <SSH_PRIVATE_KEY_PATH> [DOCKERHUB_USER]
# ==============================================================================
set -e

EC2_IP=${1:?"Error: Please provide EC2 Public IP as argument 1"}
SSH_KEY=${2:?"Error: Please provide SSH Key file path as argument 2"}
DOCKERHUB_USER=${3:-"prabhatrai05"}

echo "=========================================================="
echo "Deploying AI Investment Research Suite to EC2: $EC2_IP"
echo "Docker Hub User: $DOCKERHUB_USER"
echo "=========================================================="

# 1. Sync production docker-compose and monitoring configs to EC2
echo "[1/4] Copying Compose & Telemetry configurations to EC2..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ubuntu@"$EC2_IP" "mkdir -p ~/app/monitoring"
scp -i "$SSH_KEY" -r ./docker-compose.prod.yml ubuntu@"$EC2_IP":~/app/
scp -i "$SSH_KEY" -r ./monitoring ubuntu@"$EC2_IP":~/app/

# 2. Pull latest images and restart containers
echo "[2/4] Pulling production images from Docker Hub..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ubuntu@"$EC2_IP" << EOF
    cd ~/app
    export DOCKERHUB_USER="$DOCKERHUB_USER"
    docker compose -f docker-compose.prod.yml pull
    echo "[3/4] Starting updated containers..."
    docker compose -f docker-compose.prod.yml up -d --remove-orphans
    echo "[4/4] Pruning legacy dangling images..."
    docker image prune -f
    echo "Current Container Status:"
    docker compose -f docker-compose.prod.yml ps
EOF

echo "=========================================================="
echo "Deployment Finished. Verifying Health..."
echo "=========================================================="
curl -s --retry 5 --retry-delay 3 http://"$EC2_IP":5005/health || echo "Note: Backend is still warming up..."
echo -e "\nApplication Live at: http://$EC2_IP"
echo "Grafana Dashboard:   http://$EC2_IP:3002 (admin/admin)"
