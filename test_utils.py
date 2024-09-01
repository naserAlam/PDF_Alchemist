from time import time
from utils.pdf_utils import pdf_to_images, process_pdfs_in_batches

SAMPLE_FILE = "uploads\\sample_file\\System Desgin Handbook.pdf"
# OUTPUT_FOLDER = "converted_images\\"
OUTPUT_FOLDER = "C:\\Users\\naser\\Desktop\\batch_test"
PDF_DIR = "D:\\Downloads"

# imgs = pdf_to_images(pdf_path=SAMPLE_FILE, output_folder=OUTPUT_FOLDER)

# for path in imgs:
#     print(path)

start_time = time() 
process_pdfs_in_batches(directory=PDF_DIR, output_folder=OUTPUT_FOLDER)
execution_time = math.ceil(time() - start_time)
print(f'Execution time {execution_time} seconds (approx.)')