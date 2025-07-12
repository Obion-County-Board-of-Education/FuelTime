@echo off
REM Run the Flask app for Obion County Schools Fuel Report
cd /d "%~dp0"

echo ===========================================
echo Starting Obion County Schools Fuel Report
echo ===========================================
echo.

REM Check if required files exist
if not exist "app.py" (
    echo ERROR: app.py not found!
    echo Make sure you're running this from the correct directory.
    pause
    exit /b 1
)

if not exist "templates\fuel_form.html" (
    echo ERROR: templates\fuel_form.html not found!
    echo Make sure all template files are present.
    pause
    exit /b 1
)

REM Create temp directory if it doesn't exist
if not exist "temp" mkdir temp

echo Starting Flask application...
echo.
echo The application will be available at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask app
python app.py

echo.
echo Flask app has stopped.
pause
