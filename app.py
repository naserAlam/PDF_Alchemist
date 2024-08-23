from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from config import UPLOAD_FOLDER, OUTPUT_FOLDER, ALLOWED_EXTENSIONS
from utils.pdf_utils import allowed_file, pdf_to_images

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return 'App Created'

@app.route('/convert_pdf', methods=['POST'])
def convert_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Convert PDF to images
        image_paths = pdf_to_images(file_path, app.config['OUTPUT_FOLDER'], filename)

        # Return paths of the generated images
        return jsonify({"image_paths": image_paths}), 200

    return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)