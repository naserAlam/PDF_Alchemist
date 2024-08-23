import os

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'converted_images'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure the upload and output folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
