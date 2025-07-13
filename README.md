# FuelTime - Obion County Schools Forms Portal

A web-based application for fuel reporting and timesheet management with professional PDF generation.

## 🚀 Quick Deploy with Docker

### For Users (Deploy from GitHub)

1. **Create a new directory**:
   ```bash
   mkdir fueltime-app
   cd fueltime-app
   ```

2. **Create a `docker-compose.yml` file** with this content:
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
         - ./temp:/app/temp
       restart: unless-stopped
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:5000/"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 40s
   ```

3. **Start the application**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**: `http://localhost:5000`

5. **Stop the application**:
   ```bash
   docker-compose down
   ```

### For Developers (Local Development)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Obion-County-Board-of-Education/FuelTime.git
   cd FuelTime
   ```

2. **Start with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**: `http://localhost:5000`

## ✨ Features

- **Fuel Sheet Management**: Monthly fuel consumption tracking with vehicle information
- **Timesheet Management**: Employee hours tracking with auto-fill calendar functionality
- **PDF Generation**: Professional PDF export for both fuel sheets and timesheets
- **Digital Signatures**: Add signatures to timesheets for authentication
- **Auto-fill Calendar**: Smart date population for timesheet scheduling
- **Hour Calculations**: Automatic total hours calculation with business logic
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Containerized Deployment**: Easy Docker-based deployment with no manual setup

## 📋 Application Structure

- **Fuel Sheet Tab**: Enter monthly fuel data, vehicle information, and daily usage
- **Timesheet Tab**: Track daily work hours with automatic date population
- **PDF Export**: Generate professional reports for printing or digital storage
- **Digital Signatures**: Canvas-based signature drawing and file upload support

## 🔧 Prerequisites

- Docker and Docker Compose installed
- Internet connection (for GitHub repository access)
- Modern web browser

### Install Docker
- **Windows/Mac**: [Docker Desktop](https://docs.docker.com/get-docker/)
- **Ubuntu**: `sudo apt update && sudo apt install docker.io docker-compose`
- **CentOS/RHEL**: `sudo yum install docker docker-compose`

## 🐳 Docker Commands

| Command | Purpose |
|---------|---------|
| `docker-compose up -d` | Start in background |
| `docker-compose down` | Stop the application |
| `docker-compose logs -f` | View real-time logs |
| `docker-compose ps` | Check container status |
| `docker-compose pull` | Update to latest version |
| `docker-compose restart` | Restart the application |

## 🛠️ Customization

### Custom Port
To run on a different port, modify the docker-compose.yml:
```yaml
ports:
  - "8080:5000"  # Use port 8080 instead
```

### Environment Variables
Available environment options:
```yaml
environment:
  - FLASK_ENV=production     # or development
  - FLASK_DEBUG=false        # or true for development
```

## 📁 File Structure

```
FuelTime/
├── app.py                        # Main Flask application
├── templates/
│   ├── fuel_form.html           # Main form interface
│   ├── pdf_template.html        # Fuel sheet PDF template
│   └── timesheet_pdf_template.html  # Timesheet PDF template
├── static/
│   └── logo.png                 # Application logo
├── temp/                        # PDF storage (auto-created)
├── docker-compose.yml          # Development Docker config
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚨 Troubleshooting

### Application Won't Start
1. **Check Docker is running**: Ensure Docker Desktop is started
2. **Port conflicts**: Change port in docker-compose.yml if 5000 is in use
3. **View logs**: `docker-compose logs -f fueltime`
4. **Rebuild**: `docker-compose up --build`

### PDF Generation Issues
1. **Check container health**: `docker-compose ps`
2. **Restart application**: `docker-compose restart`
3. **View detailed logs**: `docker-compose logs fueltime`

### Updates Not Showing
1. **Pull latest changes**: `docker-compose pull`
2. **Restart with latest**: `docker-compose up -d`
3. **Force rebuild**: `docker-compose build --no-cache`

## 📞 Support

**Obion County Schools IT Department**
- Email: jhowell@ocboe.com
- For technical issues, include:
  - Output from `docker-compose logs`
  - Steps to reproduce the issue
  - Browser and operating system information

## 📜 License

This application is proprietary software of Obion County Schools.
