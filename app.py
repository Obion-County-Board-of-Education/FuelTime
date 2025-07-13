from flask import Flask, render_template, request, jsonify, send_file
import pdfkit
import tempfile
import os
from datetime import datetime
import logging
import subprocess

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Check if wkhtmltopdf is available
def check_wkhtmltopdf():
    """Check if wkhtmltopdf is installed and accessible"""
    try:
        subprocess.run(['wkhtmltopdf', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Set wkhtmltopdf path for Windows if needed
WKHTMLTOPDF_INSTALLED = check_wkhtmltopdf()
if not WKHTMLTOPDF_INSTALLED:
    # Try common Windows installation paths
    possible_paths = [
        r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe',
        r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
    ]
    for path in possible_paths:
        if os.path.exists(path):
            pdfkit_config = pdfkit.configuration(wkhtmltopdf=path)
            WKHTMLTOPDF_INSTALLED = True
            break
    else:
        pdfkit_config = None
else:
    pdfkit_config = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Serve the main form page"""
    # Load logo as base64 for embedding
    import base64
    import os
    logo_base64 = None
    try:
        logo_path = os.path.join(app.static_folder, 'logo.png')
        with open(logo_path, 'rb') as f:
            logo_data = base64.b64encode(f.read()).decode()
            logo_base64 = f"data:image/png;base64,{logo_data}"
    except Exception as e:
        logger.error(f"Error loading logo: {e}")
    
    return render_template('fuel_form.html', logo_base64=logo_base64)

@app.route('/submit', methods=['POST'])
def submit_form():
    """Process form submission and generate PDF"""
    try:
        # Get form data
        form_data = request.json
        logger.info(f"Received form data for {form_data.get('name', 'Unknown')}")
        
        # Generate PDF
        pdf_path = generate_pdf(form_data)
        
        # Move PDF to a permanent location for download
        download_filename = f"FuelReport_{form_data.get('name', 'Unknown')}_{form_data.get('month', '')}_{form_data.get('year', '')}.pdf"
        download_path = os.path.join('/app/temp', download_filename)
        
        # Copy the file instead of renaming to avoid cross-device issues
        import shutil
        shutil.copy2(pdf_path, download_path)
        os.unlink(pdf_path)  # Remove original temp file
        
        return jsonify({
            'success': True,
            'message': 'Fuel report generated successfully! Click below to download.',
            'download_url': f'/download/{download_filename}'
        })
        
    except Exception as e:
        logger.error(f"Error processing form submission: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error generating report: {str(e)}'
        }), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Serve generated PDF files"""
    try:
        file_path = os.path.join('/app/temp', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_pdf(form_data):
    """Generate PDF from form data"""
    try:
        # Check if wkhtmltopdf is available (Docker should have it installed)
        if not WKHTMLTOPDF_INSTALLED:
            raise Exception("wkhtmltopdf is not installed. Please check Docker image setup.")
        
        # Render the filled form as HTML
        filled_html = render_template('pdf_template.html', form_data=form_data)
        
        # Create temporary file for PDF - use Docker temp directory
        temp_dir = '/app/temp'
        os.makedirs(temp_dir, exist_ok=True)
        
        pdf_filename = f"temp_fuel_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        # Configure PDF options for high quality output - optimized for maximum content size
        options = {
            'page-size': 'Letter',
            'orientation': 'Portrait',
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.2in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
            'disable-smart-shrinking': None,
            'zoom': 1.0,
            'dpi': 300,
            'image-quality': 100,
            'disable-javascript': None,
            'load-media-error-handling': 'ignore'
        }
        
        # Generate PDF with proper configuration
        if pdfkit_config:
            pdfkit.from_string(filled_html, pdf_path, options=options, configuration=pdfkit_config)
        else:
            pdfkit.from_string(filled_html, pdf_path, options=options)
            
        logger.info(f"PDF generated successfully at {pdf_path}")
        
        return pdf_path
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise

@app.route('/preview-pdf', methods=['POST'])
def preview_pdf():
    """Generate and return PDF for preview/download"""
    try:
        form_data = request.json
        pdf_path = generate_pdf(form_data)
        
        # Return PDF file
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"FuelReport_{form_data.get('name', 'Unknown')}_{form_data.get('month', '')}_{form_data.get('year', '')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"Error generating PDF preview: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error generating PDF: {str(e)}'
        }), 500

@app.route('/logo')
def serve_logo():
    """Serve the logo file directly"""
    from flask import make_response
    response = make_response(send_file('static/logo.png', mimetype='image/png'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/logo-data')
def serve_logo_data():
    """Serve the logo as base64 data URL"""
    import base64
    import os
    try:
        logo_path = os.path.join(app.static_folder, 'logo.png')
        with open(logo_path, 'rb') as f:
            logo_data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{logo_data}"
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/test-logo')
def test_logo():
    """Test route to check if logo file exists"""
    import os
    logo_path = os.path.join(app.static_folder, 'logo.png')
    exists = os.path.exists(logo_path)
    return {
        'logo_path': logo_path,
        'exists': exists,
        'static_folder': app.static_folder,
        'static_url_path': app.static_url_path
    }

@app.route('/debug-logo')
def debug_logo():
    """Debug route to check logo loading"""
    import base64
    import os
    
    logo_path = os.path.join(app.static_folder, 'logo.png')
    file_exists = os.path.exists(logo_path)
    
    if file_exists:
        file_size = os.path.getsize(logo_path)
        try:
            with open(logo_path, 'rb') as f:
                logo_data = base64.b64encode(f.read()).decode()
            data_url = f"data:image/png;base64,{logo_data}"
            
            return f"""
            <h1>Logo Debug Info</h1>
            <p>File exists: {file_exists}</p>
            <p>File size: {file_size} bytes</p>
            <p>Base64 length: {len(logo_data)} characters</p>
            <p>Data URL length: {len(data_url)} characters</p>
            <p>First 100 chars: {data_url[:100]}...</p>
            <h2>Test Image:</h2>
            <img src="{data_url}" alt="Test Logo" width="400" height="150" style="border: 2px solid red;">
            """
        except Exception as e:
            return f"Error reading file: {e}"
    else:
        return f"Logo file does not exist at: {logo_path}"

@app.route('/test-simple-image')
def test_simple_image():
    """Test with a tiny base64 image"""
    # This is a tiny 1x1 red pixel PNG
    tiny_red_pixel = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    return f"""
    <h1>Simple Image Test</h1>
    <h2>Tiny Red Pixel (should show a 1x1 red dot):</h2>
    <img src="data:image/png;base64,{tiny_red_pixel}" alt="Red Pixel" width="100" height="100" style="border: 2px solid blue; image-rendering: pixelated;">
    
    <h2>Blue Square (inline SVG for comparison):</h2>
    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iYmx1ZSIvPjwvc3ZnPg==" alt="Blue Square" width="100" height="100" style="border: 2px solid green;">
    """

@app.route('/submit-timesheet', methods=['POST'])
def submit_timesheet():
    """Process timesheet form submission and generate PDF"""
    try:
        # Get form data
        form_data = request.json
        logger.info(f"Received timesheet data for {form_data.get('emp_name', 'Unknown')}")
        
        # Add date fields from the form (extract from date fields in the table)
        timesheet_data = {}
        
        # Copy all the form data
        for key, value in form_data.items():
            timesheet_data[key] = value
        
        # Extract dates from the date fields and add them to the data
        for week in range(1, 6):  # 5 weeks
            for day in ['m', 't', 'w', 'th', 'f']:
                date_key = f'date_{day}{week}'
                if date_key in form_data:
                    timesheet_data[date_key] = form_data[date_key]
        
        # Calculate total days worked
        total_days = 0
        for key, value in form_data.items():
            if key.startswith('total_hours_') and value and value.strip():
                try:
                    hours = float(value)
                    if hours > 0:
                        total_days += 1
                except (ValueError, TypeError):
                    pass
        
        timesheet_data['total_days'] = str(total_days)
        
        # Generate PDF
        pdf_path = generate_timesheet_pdf(timesheet_data)
        
        # Move PDF to a permanent location for download
        download_filename = f"Timesheet_{timesheet_data.get('emp_name', 'Unknown')}_{timesheet_data.get('time_period', '').replace('/', '_').replace(' ', '_')}.pdf"
        download_path = os.path.join('/app/temp', download_filename)
        
        # Copy the file instead of renaming to avoid cross-device issues
        import shutil
        shutil.copy2(pdf_path, download_path)
        os.unlink(pdf_path)  # Remove original temp file
        
        return jsonify({
            'success': True,
            'message': 'Timesheet generated successfully! Click below to download.',
            'download_url': f'/download/{download_filename}'
        })
        
    except Exception as e:
        logger.error(f"Error processing timesheet submission: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error generating timesheet: {str(e)}'
        }), 500

def generate_timesheet_pdf(form_data):
    """Generate PDF from timesheet form data"""
    try:
        # Check if wkhtmltopdf is available (Docker should have it installed)
        if not WKHTMLTOPDF_INSTALLED:
            raise Exception("wkhtmltopdf is not installed. Please check Docker image setup.")
        
        # Render the filled timesheet as HTML
        filled_html = render_template('timesheet_pdf_template.html', form_data=form_data)
        
        # Create temporary file for PDF - use Docker temp directory
        temp_dir = '/app/temp'
        os.makedirs(temp_dir, exist_ok=True)
        
        pdf_filename = f"temp_timesheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        # Configure PDF options for timesheet - optimized for single page
        options = {
            'page-size': 'Letter',
            'orientation': 'Portrait',
            'margin-top': '0.3in',
            'margin-right': '0.3in',
            'margin-bottom': '0.3in',
            'margin-left': '0.3in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
            'disable-smart-shrinking': None,
            'zoom': 1.0,  # Use full zoom for maximum content
            'dpi': 300,
            'image-quality': 100,
            'disable-javascript': None,
            'load-media-error-handling': 'ignore',
            'minimum-font-size': 8  # Allow small fonts for compact layout
        }
        
        # Generate PDF with proper configuration
        if pdfkit_config:
            pdfkit.from_string(filled_html, pdf_path, options=options, configuration=pdfkit_config)
        else:
            pdfkit.from_string(filled_html, pdf_path, options=options)
            
        logger.info(f"Timesheet PDF generated successfully at {pdf_path}")
        
        return pdf_path
        
    except Exception as e:
        logger.error(f"Error generating timesheet PDF: {str(e)}")
        raise

@app.route('/preview-timesheet-pdf', methods=['POST'])
def preview_timesheet_pdf():
    """Generate and return timesheet PDF for preview/download"""
    try:
        form_data = request.json
        
        # Process the form data similarly to submit_timesheet
        timesheet_data = {}
        
        # Copy all the form data
        for key, value in form_data.items():
            timesheet_data[key] = value
        
        # Calculate total days worked
        total_days = 0
        for key, value in form_data.items():
            if key.startswith('total_hours_') and value and value.strip():
                try:
                    hours = float(value)
                    if hours > 0:
                        total_days += 1
                except (ValueError, TypeError):
                    pass
        
        timesheet_data['total_days'] = str(total_days)
        
        pdf_path = generate_timesheet_pdf(timesheet_data)
        
        # Return PDF file
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"Timesheet_{timesheet_data.get('emp_name', 'Unknown')}_{timesheet_data.get('time_period', '').replace('/', '_').replace(' ', '_')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"Error generating timesheet PDF preview: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error generating timesheet PDF: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
