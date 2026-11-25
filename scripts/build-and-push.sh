#!/bin/bash
set -e

echo "========================================================"
echo "  Building and Pushing Docker Images to Docker Hub"
echo "  Repository: prabhatrai05"
echo "========================================================"

echo ""
echo "[Step 1/5] Authenticating with Docker Hub..."
echo "@Prabhat0528" | docker login -u prabhatrai05 --password-stdin

echo ""
echo "[Step 2/5] Building Backend Docker Image..."
docker build -t prabhatrai05/ai-investment-backend:latest ./backend

echo ""
echo "[Step 3/5] Building Frontend Docker Image (Production Multi-Stage)...
docker build -t prabhatrai05/ai-investment-frontend:latest -f ./frontend/Dockerfile.prod ./frontend

echo ""
echo "[Step 4/5] Pushing Backend Image to Docker Hub..."
docker push prabhatrai05/ai-investment-backend:latest

echo ""
echo "[Step 5/5] Pushing Frontend Image to Docker Hub..."
docker push prabhatrai05/ai-investment-frontend:latest

echo ""
echo "========================================================"
echo "  SUCCESS! Both Docker images are published to Docker Hub:"
echo "  - prabhatrai05/ai-investment-backend:latest"
echo "  - prabhatrai05/ai-investment-frontend:latest"
echo "========================================================"
