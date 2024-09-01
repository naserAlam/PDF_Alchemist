import fitz
import os
import logging
import time
import math
from queue import Queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


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
    print(f'Output folder: {subfolder_path} \n')

    start_time = time.time()
    for page_num in range(total_pages):
        try:
            page = pdf_document[page_num]
            pix = page.get_pixmap(dpi=500)

            output_image_path = os.path.join(subfolder_path, f'page_{page_num + 1}.{image_format}')
            pix.save(output_image_path)
            image_paths.append(output_image_path)
        except Exception as e:
            logging.error(f'Error processing page {page_num + 1} of PDF file {pdf_path}: {e}')
    execution_time = math.ceil(time.time() - start_time)
    print(f'Execution time: {time.time() - start_time}')
    logging.info(f'Converted {file_name} successfully.')
    print(f'Converted {file_name} successfully.')
    return image_paths

def list_pdf_files(directory_path, batch_size=50):
    """
    Generator function to list PDF files in batches from a specified directory.
    :param directory_path: Path to the directory where PDF files are located.
    :param batch_size: Number of PDF files to return in each batch.
    :return: Yields a list of PDF file paths.
    """
    all_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.pdf')]
    total_files = len(all_files)
    print(f'Total {total_files} pdf files found in {directory_path}')

    for i in range(0, total_files, batch_size):
        yield all_files[i:i + batch_size]

def add_files_to_queue(file_list, queue):
    """
    Add a list of file paths to the queue.
    :param file_list: List of PDF file paths.
    :param queue: Queue object to store file paths.
    """
    for file_path in file_list:
        queue.put(file_path)

def worker(queue, output_folder):
    """
    Worker function to process PDF files from the queue.
    """
    while not queue.empty():
        pdf_path = queue.get()
        file_name = os.path.basename(pdf_path)
        pdf_to_images(pdf_path, output_folder, file_name=file_name)
        queue.task_done()

def process_pdfs_in_batches(directory, output_folder, batch_size=50, num_workers=5):
    """
    Process PDF files in batches and convert them to images using multiple workers.
    :param directory: Directory containing PDF files.
    :param output_folder: Directory to save the output images.
    :param batch_size: Number of PDF files to process in each batch.
    :param num_workers: Number of worker threads to process the PDFs concurrently.
    """
    pdf_queue = Queue()

    for pdf_batch in list_pdf_files(directory, batch_size):
        add_files_to_queue(pdf_batch, pdf_queue)

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            for _ in range(num_workers):
                executor.submit(worker, pdf_queue, output_folder)

        pdf_queue.join()