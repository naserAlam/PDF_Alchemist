from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from config import UPLOAD_FOLDER, OUTPUT_FOLDER, ALLOWED_EXTENSIONS
from utils.pdf_utils import pdf_to_images

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return 'App Created'

@app.route('/convert_pdf', methods=['POST'])
def convert_pdf():
    file = request.files['file']

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    image_paths = pdf_to_images(file_path, app.config['OUTPUT_FOLDER'], filename)

    return jsonify({"image_paths": image_paths}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)