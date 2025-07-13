#!/bin/bash

# FuelTime Quick Deploy Script
# This script creates a docker-compose.yml and starts the FuelTime application

echo "🚀 FuelTime Quick Deploy"
echo "========================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose found"

# Create deployment directory
DEPLOY_DIR="fueltime-app"
if [ ! -d "$DEPLOY_DIR" ]; then
    mkdir "$DEPLOY_DIR"
    echo "📁 Created deployment directory: $DEPLOY_DIR"
fi

cd "$DEPLOY_DIR"

# Create docker-compose.yml file
echo "� Creating docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  fueltime:
    build:
      context: https://github.com/Obion-County-Board-of-Education/FuelTime.git
      dockerfile: Dockerfile
    container_name: fueltime-app
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=false
    volumes:
      - ./temp:/app/temp
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
EOF

echo "✅ docker-compose.yml created"

# Create temp directory
mkdir -p temp
echo "📁 Created temp directory for PDFs"

# Start the application
echo "🐳 Starting FuelTime application..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 FuelTime is now running!"
    echo ""
    echo "🌐 Access the application at: http://localhost:5000"
    echo ""
    echo "📋 Management commands:"
    echo "   View logs:     docker-compose logs -f"
    echo "   Stop app:      docker-compose down"
    echo "   Restart:       docker-compose restart"
    echo "   Update:        docker-compose pull && docker-compose up -d"
    echo ""
    echo "📁 Files created in: $(pwd)"
else
    echo "❌ Failed to start the application"
    echo "Check logs with: docker-compose logs"
    exit 1
fi
