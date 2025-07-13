@echo off
REM FuelTime App Deployment Script for Windows
REM This script helps deploy the FuelTime application using Docker

echo 🚀 FuelTime App Deployment Script
echo ==================================

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
    echo ❌ Docker Compose is not installed. Please install Docker Desktop first.
    echo Visit: https://docs.docker.com/desktop/windows/
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Create deployment directory
set DEPLOY_DIR=fueltime-deployment
if not exist "%DEPLOY_DIR%" (
    mkdir "%DEPLOY_DIR%"
    echo 📁 Created deployment directory: %DEPLOY_DIR%
)

cd "%DEPLOY_DIR%"

REM Download the production docker-compose file
echo 📥 Downloading production configuration...
curl -s -o docker-compose.yml https://raw.githubusercontent.com/Obion-County-Board-of-Education/FuelTime/main/docker-compose.prod.yml

if %errorlevel% equ 0 (
    echo ✅ Configuration downloaded successfully
) else (
    echo ❌ Failed to download configuration
    pause
    exit /b 1
)

REM Create temp directory for persistent storage
if not exist "temp" mkdir temp

echo.
echo 🐳 Starting FuelTime application...
docker-compose up -d

if %errorlevel% equ 0 (
    echo.
    echo 🎉 FuelTime application is now running!
    echo.
    echo 📍 Access the application at: http://localhost:5000
    echo.
    echo 📋 Useful commands:
    echo    View logs:     docker-compose logs -f
    echo    Stop app:      docker-compose down
    echo    Update app:    docker-compose pull ^&^& docker-compose up -d
    echo    Check status:  docker-compose ps
    echo.
) else (
    echo ❌ Failed to start the application
    echo Check the logs with: docker-compose logs
    pause
    exit /b 1
)

pause
