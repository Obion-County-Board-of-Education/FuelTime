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
    return render_template('fuel_form.html')

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
        
        # Configure PDF options for high quality output
        options = {
            'page-size': 'Letter',
            'orientation': 'Portrait',
            'margin-top': '0.4in',
            'margin-right': '0.4in',
            'margin-bottom': '0.4in',
            'margin-left': '0.4in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
            'disable-smart-shrinking': None,
            'zoom': 0.9,
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
