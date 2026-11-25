@echo off
REM ==============================================================================
REM Script: verify-health.bat
REM Purpose: Windows Health & Smoke Test for Deployed Microservices Stack
REM Usage: verify-health.bat [HOST]
REM ==============================================================================
setlocal enabledelayedexpansion

set HOST=%1
if "%HOST%"=="" set HOST=localhost

echo ==========================================================
echo Running Microservices Health & Smoke Test for Host: %HOST%
echo ==========================================================

echo [1/5] Checking Backend API Health (http://%HOST%:5005/health)...
curl -s -o NUL -w "Status Code: %%{http_code}\n" --connect-timeout 5 http://%HOST%:5005/health

echo [2/5] Checking Backend Prometheus Metrics (http://%HOST%:5005/metrics)...
curl -s -o NUL -w "Status Code: %%{http_code}\n" --connect-timeout 5 http://%HOST%:5005/metrics

echo [3/5] Checking Frontend UI (http://%HOST%:3001)...
curl -s -o NUL -w "Status Code: %%{http_code}\n" --connect-timeout 5 http://%HOST%:3001

echo [4/5] Checking Prometheus Server Health (http://%HOST%:9090/-/healthy)...
curl -s -o NUL -w "Status Code: %%{http_code}\n" --connect-timeout 5 http://%HOST%:9090/-/healthy

echo [5/5] Checking Grafana Dashboard Health (http://%HOST%:3002/api/health)...
curl -s -o NUL -w "Status Code: %%{http_code}\n" --connect-timeout 5 http://%HOST%:3002/api/health

echo ==========================================================
echo Health Check Query Complete!
echo ==========================================================
