import fitz
import os
import logging
import time

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def pdf_to_images(pdf_path, output_folder, file_name='test', image_format='png'):
    """
    Convert a PDF file into images, one per page.
    """
    try:
        pdf_document = fitz.open(pdf_path)
    except Exception as e:
        logging.error(f'Error opening PDF file {pdf_path}: {e}')
        raise

    total_pages = len(pdf_document)
    image_paths = []

    file_name_without_ext = os.path.splitext(file_name)[0]
    subfolder_path = os.path.join(output_folder, file_name_without_ext)
    os.makedirs(subfolder_path, exist_ok=True)
    print(subfolder_path + '\n')

    # Calculate the scale factor based on DPI
    # dpi = 500
    # zoom_x = dpi / 72  # 72 is the default DPI of PDF
    # zoom_y = dpi / 72
    # matrix = fitz.Matrix(zoom_x, zoom_y)

    start_time = time.time()
    for page_num in range(total_pages):
        try:
            page = pdf_document[page_num]
            pix = page.get_pixmap(dpi=500)
            # pix = page.get_pixmap(matrix=matrix)

            output_image_path = os.path.join(subfolder_path, f'page_{page_num + 1}.{image_format}')
            pix.save(output_image_path)
            image_paths.append(output_image_path)
        except Exception as e:
            logging.error(f'Error processing page {page_num + 1} of PDF file {pdf_path}: {e}')
    print(f'Execution time: {time.time() - start_time}')
    logging.info(f'Converted {file_name} successfully.')
    print(f'Converted {file_name} successfully.')
    return image_paths
