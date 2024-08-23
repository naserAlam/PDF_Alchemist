import fitz
import os

# Configuration
UPLOAD_FOLDER = '../uploads'
OUTPUT_FOLDER = '../converted_images'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure the upload and output folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

### Sample data
SAMPLE_PDF = '../uploads/System Desgin Handbook.pdf'
OUTPUT_PATH = '../converted_images/test/'

def pdf_to_image(pdf_path, output_folder, file_name, image_format='png'):
    """
    docstring
    """
    pdf_document = fitz.open(pdf_path)
    total_pages = len(pdf_document)
    image_paths = []

    file_name_without_ext = os.path.splitext(file_name)[0]
    subfolder_path = os.path.join(output_folder, file_name_without_ext)
    os.makedirs(subfolder_path, exist_ok=True)

    for page_num in range(total_pages):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        output_image_path = os.path.join(subfolder_path, f'page_{page_num + 1}.{image_format}')
        pix.save(output_image_path)
        image_paths.append(output_image_path)

    return image_paths


print(pdf_to_image(pdf_path=SAMPLE_PDF, output_folder=OUTPUT_PATH, file_name='test'))