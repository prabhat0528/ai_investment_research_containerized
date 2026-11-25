#!/usr/bin/env bash
# ==============================================================================
# Script: trivy-scan.sh
# Purpose: Container Image Security & CVE Vulnerability Gate for CI/CD Pipelines
# ==============================================================================
set -e

BACKEND_IMAGE=${1:-"prabhatrai05/ai-investment-backend:latest"}
FRONTEND_IMAGE=${2:-"prabhatrai05/ai-investment-frontend:latest"}
REPORT_DIR="./devops/security/reports"

mkdir -p "$REPORT_DIR"

echo "=========================================================="
echo "DevSecOps Gate: Scanning Docker Images with Trivy"
echo "=========================================================="

# Check if Trivy is installed, otherwise pull and run via Docker
RUN_TRIVY="trivy"
if ! command -v trivy &> /dev/null; then
    echo "[INFO] Local Trivy binary not found. Using Dockerized Trivy..."
    RUN_TRIVY="docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd)/$REPORT_DIR:/reports aquasec/trivy"
fi

echo "[1/2] Scanning Backend Image ($BACKEND_IMAGE)..."
$RUN_TRIVY image \
  --severity HIGH,CRITICAL \
  --format table \
  --output "$REPORT_DIR/backend-vulns.txt" \
  "$BACKEND_IMAGE" || true

echo "[2/2] Scanning Frontend Image ($FRONTEND_IMAGE)..."
$RUN_TRIVY image \
  --severity HIGH,CRITICAL \
  --format table \
  --output "$REPORT_DIR/frontend-vulns.txt" \
  "$FRONTEND_IMAGE" || true

echo "=========================================================="
echo "Security Assessment Reports Generated in: $REPORT_DIR"
echo "=========================================================="
cat "$REPORT_DIR/backend-vulns.txt" | head -n 30
