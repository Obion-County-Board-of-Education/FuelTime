# Obion County Schools Forms Portal

A Dockerized web-based forms system for fuel reports and timesheets with professional PDF generation.

## 🚀 Quick Start

### Start the Application

```cmd
docker-compose up --build
```

### Access the Application

Open your browser to: **http://localhost:5000**

### Use the Application

1. **Fuel Reports Tab**: Fill out monthly fuel usage data
2. **Timesheet Tab**: Track work hours with auto-fill schedules
3. **Generate PDF**: Click "Print to PDF" to download professional reports

### Stop the Application

```cmd
docker-compose down
```

That's it! Docker handles all dependencies including wkhtmltopdf automatically.

## Features

- ✅ **Tabbed Interface**: Fuel reports and timesheets in one portal
- ✅ **Professional PDF Generation**: Server-side rendering with perfect formatting
- ✅ **Timesheet Auto-fill**: Smart scheduling for standard work hours
- ✅ **Static Calendar**: Reliable M/T/W/Th/F structure with date auto-population
- ✅ **Input Validation**: Real-time calculation and error handling
- ✅ **Responsive Design**: Works on desktop and mobile devices
- ✅ **Fully Containerized**: No manual dependency management

## Requirements

- Docker and Docker Compose
- Web browser

## Docker Commands

| Command | Purpose |
|---------|---------|
| `docker-compose up --build` | Build and start the application |
| `docker-compose up -d` | Start in background (detached mode) |
| `docker-compose down` | Stop the application |
| `docker-compose logs -f` | View real-time logs |
| `docker-compose ps` | Check container status |

## File Structure

```
fuel/
├── app.py                     # Main Flask application
├── templates/
│   ├── fuel_form.html        # Tabbed interface with forms
│   └── pdf_template.html     # PDF generation template
├── temp/                     # Temporary files (Docker volume)
├── docker-compose.yml       # Docker compose configuration
├── Dockerfile               # Docker image definition
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Troubleshooting

### "Failed to fetch" Error

1. **Check if container is running**:
   ```cmd
   docker-compose ps
   ```

2. **View container logs**:
   ```cmd
   docker-compose logs
   ```

3. **Restart the container**:
   ```cmd
   docker-compose down
   docker-compose up --build
   ```

### Other Issues

- **Port conflict**: If port 5000 is in use, change it in `docker-compose.yml`
- **Docker not running**: Make sure Docker Desktop is started
- **Build failures**: Run `docker-compose build --no-cache`

## Benefits of This Solution

- ✅ **No manual setup**: Everything is containerized
- ✅ **Cross-platform**: Works on Windows, Mac, and Linux
- ✅ **Professional PDFs**: Server-side generation with perfect formatting
- ✅ **Multiple Forms**: Fuel reports and timesheets in one application
- ✅ **Easy deployment**: Single command to start
- ✅ **Isolated environment**: No conflicts with other software

## Support

For issues:
1. Check container status: `docker-compose ps`
2. Review logs: `docker-compose logs -f`
3. Rebuild if needed: `docker-compose up --build`
