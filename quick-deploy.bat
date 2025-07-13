@echo off
REM FuelTime Quick Deploy Script for Windows

echo 🚀 FuelTime Quick Deploy
echo ========================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    echo Visit: https://docs.docker.com/desktop/windows/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not found. Please install Docker Desktop.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose found

REM Create deployment directory
set DEPLOY_DIR=fueltime-app
if not exist "%DEPLOY_DIR%" (
    mkdir "%DEPLOY_DIR%"
    echo 📁 Created deployment directory: %DEPLOY_DIR%
)

cd "%DEPLOY_DIR%"

REM Create docker-compose.yml file
echo � Creating docker-compose.yml...
(
echo version: '3.8'
echo.
echo services:
echo   fueltime:
echo     build:
echo       context: https://github.com/Obion-County-Board-of-Education/FuelTime.git
echo       dockerfile: Dockerfile
echo     container_name: fueltime-app
echo     ports:
echo       - "5000:5000"
echo     environment:
echo       - FLASK_ENV=production
echo       - FLASK_DEBUG=false
echo     volumes:
echo       - ./temp:/app/temp
echo     restart: unless-stopped
echo     healthcheck:
echo       test: ["CMD", "curl", "-f", "http://localhost:5000/"]
echo       interval: 30s
echo       timeout: 10s
echo       retries: 3
echo       start_period: 40s
) > docker-compose.yml

echo ✅ docker-compose.yml created

REM Create temp directory
if not exist "temp" mkdir temp
echo 📁 Created temp directory for PDFs

REM Start the application
echo 🐳 Starting FuelTime application...
docker-compose up -d

if %errorlevel% equ 0 (
    echo.
    echo 🎉 FuelTime is now running!
    echo.
    echo 🌐 Access the application at: http://localhost:5000
    echo.
    echo 📋 Management commands:
    echo    View logs:     docker-compose logs -f
    echo    Stop app:      docker-compose down
    echo    Restart:       docker-compose restart
    echo    Update:        docker-compose pull ^&^& docker-compose up -d
    echo.
    echo 📁 Files created in: %cd%
) else (
    echo ❌ Failed to start the application
    echo Check logs with: docker-compose logs
    pause
    exit /b 1
)

pause
