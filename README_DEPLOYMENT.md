# FuelTime App - Docker Deployment

This repository contains the FuelTime application for Obion County Schools, providing fuel reporting and timesheet management functionality.

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed on your system
- Internet connection to pull the repository

### Running the Application

1. **Download the production docker-compose file**:
   ```bash
   curl -O https://raw.githubusercontent.com/Obion-County-Board-of-Education/FuelTime/main/docker-compose.prod.yml
   ```

2. **Start the application**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Access the application**:
   Open your web browser and navigate to: `http://localhost:5000`

4. **Stop the application**:
   ```bash
   docker-compose -f docker-compose.prod.yml down
   ```

### Alternative: Clone and Run

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

3. **Access the application**:
   Open your web browser and navigate to: `http://localhost:5000`

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
