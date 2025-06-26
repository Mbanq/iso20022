#!/usr/bin/env python3
"""
ISO20022 Message Generator Web Application

This web application allows users to upload an XSD file and JSON payload
to generate ISO20022 messages.
"""

import os
import sys
import json
import tempfile
from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename

# Add the parent directory to the path to ensure imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the fedwire module functions
from miso20022.fedwire import generate_fedwire_message

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_message():
    """Generate an ISO20022 message from the uploaded XSD and JSON payload."""
    try:
        # Check if XSD file was uploaded
        if 'xsd_file' not in request.files:
            return jsonify({'error': 'No XSD file uploaded'}), 400
        
        xsd_file = request.files['xsd_file']
        if xsd_file.filename == '':
            return jsonify({'error': 'No XSD file selected'}), 400
        
        # Save the XSD file
        xsd_filename = secure_filename(xsd_file.filename)
        xsd_path = os.path.join(app.config['UPLOAD_FOLDER'], xsd_filename)
        xsd_file.save(xsd_path)
        
        # Get message code
        message_code = request.form.get('message_code')
        if not message_code:
            return jsonify({'error': 'Message code is required'}), 400
        
        # Get payload - either from file upload or text input
        payload = None
        if 'payload_file' in request.files and request.files['payload_file'].filename != '':
            payload_file = request.files['payload_file']
            payload_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(payload_file.filename))
            payload_file.save(payload_path)
            with open(payload_path, 'r') as f:
                payload = json.load(f)
        elif 'payload_text' in request.form and request.form['payload_text'].strip():
            try:
                payload = json.loads(request.form['payload_text'])
            except json.JSONDecodeError:
                return jsonify({'error': 'Invalid JSON payload'}), 400
        else:
            return jsonify({'error': 'No payload provided'}), 400
        
        # Generate the message
        app_hdr_xml, document_xml, complete_message = generate_fedwire_message(message_code, payload, xsd_path)
        
        if not complete_message:
            return jsonify({'error': 'Failed to generate message'}), 500
        
        # Save the generated message to a temporary file
        output_filename = f"{message_code.split(':')[-1]}_{os.path.basename(xsd_filename).split('.')[0]}.xml"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        with open(output_path, 'w') as f:
            f.write(complete_message)
        
        return jsonify({
            'message': 'Message generated successfully',
            'app_hdr': app_hdr_xml,
            'document': document_xml,
            'complete_message': complete_message,
            'filename': output_filename
        })
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error generating message: {str(e)}\n{error_traceback}")
        return jsonify({'error': f'Error generating message: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download the generated XML file."""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
