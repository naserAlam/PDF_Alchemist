from utils.pdf_utils import pdf_to_images

SAMPLE_FILE = "uploads\\sample_file\\System Desgin Handbook.pdf"
OUTPUT_FOLDER = "converted_images\\"

imgs = pdf_to_images(pdf_path=SAMPLE_FILE, output_folder=OUTPUT_FOLDER)

for path in imgs:
    print(path)