@echo off
echo ========================================================
echo   Building and Pushing Docker Images to Docker Hub
echo   Repository: prabhatrai05
echo ========================================================

echo.
echo [Step 1/5] Authenticating with Docker Hub...
echo @Prabhat0528| docker login -u prabhatrai05 --password-stdin
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker login failed. Please ensure Docker Desktop is running.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [Step 2/5] Building Backend Docker Image...
docker build -t prabhatrai05/ai-investment-backend:latest ./backend
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Backend build failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [Step 3/5] Building Frontend Docker Image (Production Multi-Stage)...
docker build -t prabhatrai05/ai-investment-frontend:latest -f ./frontend/Dockerfile.prod ./frontend
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Frontend build failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [Step 4/5] Pushing Backend Image to Docker Hub...
docker push prabhatrai05/ai-investment-backend:latest
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to push backend image.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [Step 5/5] Pushing Frontend Image to Docker Hub...
docker push prabhatrai05/ai-investment-frontend:latest
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to push frontend image.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================================
echo   SUCCESS! Both Docker images are published to Docker Hub:
echo   - prabhatrai05/ai-investment-backend:latest
echo   - prabhatrai05/ai-investment-frontend:latest
echo ========================================================
pause
