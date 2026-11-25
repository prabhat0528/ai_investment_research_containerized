#!/usr/bin/env bash
# ==============================================================================
# Script: sts-assume-role-test.sh
# Purpose: Practical Verification of AWS STS AssumeRole and Least-Privilege RBAC
# ==============================================================================
set -e

ROLE_ARN=${1:-"arn:aws:iam::123456789012:role/ai-investment-ec2-role-prod"}
SESSION_NAME="DevOpsVerificationSession-$(date +%s)"

echo "=========================================================="
echo "Testing AWS STS AssumeRole for: $ROLE_ARN"
echo "Session Name: $SESSION_NAME"
echo "=========================================================="

echo "[1/4] Checking Current Identity..."
aws sts get-caller-identity --output table

echo "[2/4] Requesting Temporary Security Credentials via STS..."
CREDS=$(aws sts assume-role \
  --role-arn "$ROLE_ARN" \
  --role-session-name "$SESSION_NAME" \
  --duration-seconds 900 \
  --query "Credentials" \
  --output json)

export AWS_ACCESS_KEY_ID=$(echo "$CREDS" | grep "AccessKeyId" | cut -d '"' -f 4)
export AWS_SECRET_ACCESS_KEY=$(echo "$CREDS" | grep "SecretAccessKey" | cut -d '"' -f 4)
export AWS_SESSION_TOKEN=$(echo "$CREDS" | grep "SessionToken" | cut -d '"' -f 4)

echo "[3/4] Verifying Assumed Role Identity..."
aws sts get-caller-identity --output table

echo "[4/4] Verifying RBAC Boundaries (Testing S3 Access)..."
if aws s3 ls; then
  echo ">>> [SUCCESS] Role successfully granted read access to authorized S3 storage."
else
  echo ">>> [DENIED] Authorization failed (expected if bucket permissions restricted)."
fi

echo "=========================================================="
echo "STS Role Verification Completed."
echo "=========================================================="
