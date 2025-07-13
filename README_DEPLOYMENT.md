# FuelTime App - Docker Deployment

This repository contains the FuelTime application for Obion County Schools, providing fuel reporting and timesheet management functionality.

## 🚀 Quick Start - Copy & Paste Deployment

**The easiest way to deploy FuelTime:**

1. **Create a new directory for your deployment**:
   ```bash
   mkdir fueltime-app
   cd fueltime-app
   ```

2. **Create a `docker-compose.yml` file** and copy this content into it:

   ```yaml
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
         # Local directory for PDF storage
         - ./temp:/app/temp
       restart: unless-stopped
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:5000/"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 40s
   ```

3. **Run the application**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   Open your web browser and navigate to: `http://localhost:5000`

5. **Stop the application**:
   ```bash
   docker-compose down
   ```

**That's it! 🎉** The application will automatically:
- Pull the latest code from GitHub
- Build the Docker image
- Start the FuelTime application
- Create a local `temp` folder for PDF storage

## Alternative: One-Command Deploy

If you prefer a single command, create the docker-compose.yml file and run:

```bash
# Create directory and file in one go
mkdir fueltime-app && cd fueltime-app && cat > docker-compose.yml << 'EOF'
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

# Start the application
docker-compose up -d
```

## Alternative Deployment Methods

### Method 1: Clone and Run

If you prefer to clone the repository:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Obion-County-Board-of-Education/FuelTime.git
   cd FuelTime
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

### Method 2: Custom Port

To run on a different port, modify the ports section in your docker-compose.yml:

```yaml
ports:
  - "8080:5000"  # Use port 8080 instead of 5000
```

Then access the app at `http://localhost:8080`

## Prerequisites

- Docker and Docker Compose installed on your system
- Internet connection to pull the repository

### Install Docker (if needed)
- **Windows/Mac**: [Docker Desktop](https://docs.docker.com/get-docker/)
- **Ubuntu**: `sudo apt update && sudo apt install docker.io docker-compose`
- **CentOS/RHEL**: `sudo yum install docker docker-compose`

## Features

- **Fuel Sheet Management**: Create and manage fuel consumption reports
- **Timesheet Management**: Track employee hours with auto-fill calendar functionality
- **PDF Generation**: Export both fuel sheets and timesheets as professional PDFs
- **Digital Signatures**: Add signatures to timesheets
- **Responsive Design**: Works on desktop and mobile devices

## Application Structure

- **Fuel Sheet Tab**: Enter monthly fuel consumption data with vehicle information
- **Timesheet Tab**: Track daily hours worked with automatic hour calculations
- **Auto-fill Functionality**: Populate calendar dates automatically
- **PDF Export**: Generate professional reports for printing or digital storage

## Data Persistence

The application uses Docker volumes to persist:
- Temporary PDF files
- Static assets
- User-generated content

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify the port mapping in the docker-compose file:
```yaml
ports:
  - "8080:5000"  # Use port 8080 instead
```

### PDF Generation Issues
The application includes wkhtmltopdf for PDF generation. If you encounter PDF issues:
1. Ensure Docker has sufficient memory allocated
2. Check container logs: `docker-compose logs app`

### Health Check
The application includes a health check endpoint. Monitor application status:
```bash
docker-compose ps
```

## Updates

To update to the latest version:
```bash
docker-compose pull
docker-compose up -d
```

## Support

For technical support or questions about the FuelTime application, contact:
- Obion County Schools IT Department
- Email: jhowell@ocboe.com

## License

This application is proprietary software of Obion County Schools.
