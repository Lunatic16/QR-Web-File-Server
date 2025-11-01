# QR File Server

A web application that allows you to upload files and generate QR codes for easy transfer to other devices.

## Features

- Upload files of various types (PDF, images, documents, etc.)
- Generate QR codes for direct download
- Mobile-friendly interface
- Secure file sharing

## Requirements

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone or download this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install Flask qrcode[pil] Pillow
```

## Usage

1. Run the application:

```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5001` (or the port shown in the terminal)
3. Select a file to upload
4. After upload, scan the generated QR code with your mobile device to download the file
5. Alternatively, copy the link and share it with others

## How It Works

1. You upload a file through the web interface
2. The server generates a unique URL for that file
3. A QR code is created containing the download link
4. Other devices can scan this QR code to access and download the file
5. Files are stored temporarily on the server until manually removed

## Security

- File names are randomized to prevent guessing
- Only those with the QR code or link can access the files
- Files are stored in the `uploads` directory

## Supported File Types

Currently set to "None" to allow all file types but can be modified to restrict file types by adding them to line 14 ALLOWED_EXTENSIONS in app.py

- Documents: PDF, DOC, DOCX, etc
- Images: PNG, JPG, JPEG, GIF
- Archives: ZIP, RAR
- Text files: TXT
- Video files: MP4, MKV

## Directory Structure

- `app.py`: Main Flask application
- `templates/index.html`: Main page template
- `templates/receive.html`: File download page template
- `static/style.css`: Styling for the application
- `uploads/`: Directory where uploaded files are stored (created automatically)

## License

This project is available under the MIT License.
