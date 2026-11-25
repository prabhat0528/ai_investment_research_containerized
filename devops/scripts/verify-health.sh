#!/usr/bin/env bash
# ==============================================================================
# Script: verify-health.sh
# Purpose: Comprehensive Smoke & Health Test for Deployed Microservices Stack
# Usage: ./verify-health.sh [HOST_IP]
# ==============================================================================
set -e

HOST=${1:-"localhost"}
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"

echo "=========================================================="
echo "Health & Smoke Test for Host: $HOST"
echo "=========================================================="

test_endpoint() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}
    
    echo -n "Checking $name ($url)... "
    status=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$url" || echo "FAIL")
    
    if [ "$status" == "$expected_code" ]; then
        echo -e "${GREEN}[OK - HTTP $status]${NC}"
        return 0
    else
        echo -e "${RED}[FAILED - HTTP $status, expected $expected_code]${NC}"
        return 1
    fi
}

ERRORS=0

# 1. Frontend Web App
test_endpoint "Frontend UI" "http://$HOST:80" 200 || test_endpoint "Frontend Alt" "http://$HOST:3001" 200 || ERRORS=$((ERRORS + 1))

# 2. Backend REST API Health Endpoint
test_endpoint "Backend API /health" "http://$HOST:5005/health" 200 || ERRORS=$((ERRORS + 1))

# 3. Backend Prometheus Metrics Instrumentation
test_endpoint "Backend /metrics Telemetry" "http://$HOST:5005/metrics" 200 || ERRORS=$((ERRORS + 1))

# 4. Prometheus Engine UI
test_endpoint "Prometheus Server" "http://$HOST:9090/-/healthy" 200 || ERRORS=$((ERRORS + 1))

# 5. Grafana Analytics UI
test_endpoint "Grafana Dashboard" "http://$HOST:3002/api/health" 200 || ERRORS=$((ERRORS + 1))

echo "=========================================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}ALL HEALTH CHECKS PASSED PERFECTLY (5/5 Services Active)!${NC}"
    exit 0
else
    echo -e "${RED}$ERRORS SERVICES FAILED SMOKE TESTING. Verify container logs!${NC}"
    exit 1
fi
