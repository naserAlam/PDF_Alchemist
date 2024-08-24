from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from config import UPLOAD_FOLDER, OUTPUT_FOLDER, ALLOWED_EXTENSIONS
from utils.pdf_utils import allowed_file, pdf_to_images

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    return 'App Created'

@app.route('/convert_pdf', methods=['POST'])
def convert_pdf():
    if 'file' not in request.files:
        logging.error('No file part in request')
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        logging.error('No selected file')
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Convert PDF to images
            image_paths = pdf_to_images(file_path, app.config['OUTPUT_FOLDER'], filename)

            # Return paths of the generated images
            return jsonify({"image_paths": image_paths}), 200

        except Exception as e:
            logging.error(f'Error during PDF conversion: {e}')
            return jsonify({"error": "Internal server error"}), 500

    logging.error('Invalid file format')
    return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
