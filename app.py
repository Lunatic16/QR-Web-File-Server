from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import os
import qrcode
import uuid
from io import BytesIO
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
# Allow all file types by setting this to None
ALLOWED_EXTENSIONS = None
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    # Allow all file types if ALLOWED_EXTENSIONS is None
    if ALLOWED_EXTENSIONS is None:
        return True
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_qr_code(data):
    """Generate a QR code for the provided data"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + '_' + filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Generate a URL for the file download
        file_url = request.url_root + 'download/' + unique_filename
        qr_code = generate_qr_code(file_url)
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'qr_code': qr_code,
            'file_url': file_url
        })
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

@app.route('/receive')
def receive():
    """Page where users can receive files"""
    return render_template('receive.html')

@app.route('/receive_file', methods=['POST'])
def receive_file():
    """Endpoint to receive files from other users"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + '_' + filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Generate a URL for the file download
        file_url = request.url_root + 'download/' + unique_filename
        qr_code = generate_qr_code(file_url)
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'qr_code': qr_code,
            'file_url': file_url
        })
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/receive/<filename>')
def view_received_file(filename):
    """Page to view a specific received file"""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        qr_code = generate_qr_code(request.url_root + 'download/' + filename)
        return render_template('receive.html', filename=filename, qr_code=qr_code)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)