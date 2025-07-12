# Obion County Schools Fuel Report - Quick Start Guide

## Current Issue: "Failed to fetch" Error

The "Failed to fetch" error occurs because the Flask server isn't running. Here's how to fix it:

## Step 1: Install wkhtmltopdf (Required for PDF generation)

1. Go to: https://wkhtmltopdf.org/downloads.html
2. Download the Windows installer (choose 32-bit or 64-bit based on your system)
3. Run the installer and follow the setup wizard
4. **Important**: During installation, make sure to check "Add to PATH" if the option is available

## Step 2: Set Up and Run the Application

### Option A: Use the Setup Scripts (Recommended)
1. Double-click `setup_flask_app.bat` to install dependencies and check your setup
2. If wkhtmltopdf is missing, install it (see Step 1) and run the setup again
3. Once setup is complete, double-click `run_flask_app.bat` to start the server
4. Open your browser to: http://localhost:5000

### Option B: Manual Setup
```cmd
# Install Python packages
pip install Flask pdfkit python-dotenv Werkzeug

# Start the Flask server
python app.py
```

## Step 3: Access the Application

1. Open your web browser
2. Go to: http://localhost:5000
3. Fill out the fuel report form
4. Use "Print to PDF" button (should now work)
5. Use "Submit via Email" if you have configured SMTP settings

## Troubleshooting

### If you still get "Failed to fetch":
1. Make sure the Flask server is running (you should see output like "Running on http://127.0.0.1:5000")
2. Check that you can access http://localhost:5000 in your browser
3. Make sure wkhtmltopdf is properly installed

### To test wkhtmltopdf installation:
Open Command Prompt and run:
```cmd
wkhtmltopdf --version
```
If this shows version information, wkhtmltopdf is properly installed.

### If wkhtmltopdf command is not found:
1. Reinstall wkhtmltopdf and make sure to add it to PATH
2. Or manually add the installation directory to your PATH environment variable
3. Typical installation path: `C:\Program Files\wkhtmltopdf\bin\`

## Email Configuration (Optional)

To enable email functionality, create a `.env` file with:
```
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=your-email@ocboe.com
SMTP_PASSWORD=your-app-password
RECIPIENT_EMAIL=jhowell@ocboe.com
```

Note: Use an App Password, not your regular password. See `EMAIL_SETUP_GUIDE.md` for details.

## Files Overview

- `app.py` - Main Flask application
- `templates/fuel_form.html` - Web form interface  
- `templates/pdf_template.html` - PDF template
- `run_flask_app.bat` - Start the Flask server
- `setup_flask_app.bat` - Install dependencies and check setup
- `temp/` - Temporary files directory (created automatically)
