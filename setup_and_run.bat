@echo off
REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Setting up Python environment for PDF generation...
echo Current directory: %CD%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing Python...
    winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    echo.
    echo Python installation complete. Please restart your terminal and run this script again.
    pause
    exit /b
)

echo Python found. Installing ReportLab library...
python -m pip install reportlab

echo.
echo Running PDF generator...
echo Looking for: %CD%\create_fillable_pdf_simple.py
python "%CD%\create_fillable_pdf_simple.py"

echo.
echo PDF will be saved as: %CD%\obion-county-fuel-report-fillable.pdf
echo PDF generation complete!
pause
