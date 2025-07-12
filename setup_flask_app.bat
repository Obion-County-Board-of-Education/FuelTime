@echo off
REM Setup script for Obion County Schools Fuel Report Flask App
cd /d "%~dp0"

echo ===========================================
echo Obion County Schools Fuel Report Setup
echo ===========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+ first.
    echo You can download it from: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo Python found successfully!
echo.

REM Install Python packages
echo Installing Python packages...
pip install Flask pdfkit python-dotenv Werkzeug
echo.

REM Check if wkhtmltopdf is installed
echo Checking for wkhtmltopdf...
wkhtmltopdf --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: wkhtmltopdf not found!
    echo This is required for PDF generation.
    echo.
    echo Please download and install wkhtmltopdf from:
    echo https://wkhtmltopdf.org/downloads.html
    echo.
    echo Choose the Windows installer for your system (32-bit or 64-bit)
    echo After installation, restart this script.
    echo.
    pause
    exit /b 1
) else (
    wkhtmltopdf --version
    echo wkhtmltopdf found successfully!
)

echo.
echo ===========================================
echo Setup Complete!
echo ===========================================
echo.
echo To start the Fuel Report application:
echo 1. Run: run_flask_app.bat
echo 2. Or manually run: python app.py
echo 3. Then open your browser to: http://localhost:5000
echo.
pause
