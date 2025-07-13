#!/bin/bash

# FuelTime App Deployment Script
# This script helps deploy the FuelTime application using Docker

echo "🚀 FuelTime App Deployment Script"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create deployment directory
DEPLOY_DIR="fueltime-deployment"
if [ ! -d "$DEPLOY_DIR" ]; then
    mkdir "$DEPLOY_DIR"
    echo "📁 Created deployment directory: $DEPLOY_DIR"
fi

cd "$DEPLOY_DIR"

# Download the production docker-compose file
echo "📥 Downloading production configuration..."
curl -s -o docker-compose.yml https://raw.githubusercontent.com/Obion-County-Board-of-Education/FuelTime/main/docker-compose.prod.yml

if [ $? -eq 0 ]; then
    echo "✅ Configuration downloaded successfully"
else
    echo "❌ Failed to download configuration"
    exit 1
fi

# Create temp directory for persistent storage
mkdir -p temp

echo ""
echo "🐳 Starting FuelTime application..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 FuelTime application is now running!"
    echo ""
    echo "📍 Access the application at: http://localhost:5000"
    echo ""
    echo "📋 Useful commands:"
    echo "   View logs:     docker-compose logs -f"
    echo "   Stop app:      docker-compose down"
    echo "   Update app:    docker-compose pull && docker-compose up -d"
    echo "   Check status:  docker-compose ps"
    echo ""
else
    echo "❌ Failed to start the application"
    echo "Check the logs with: docker-compose logs"
    exit 1
fi
