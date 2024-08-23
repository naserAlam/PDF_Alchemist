import fitz

### Sample data
SAMPLE_PDF = '../uploads/System Desgin Handbook.pdf'
OUTPUT_PATH = '../converted_images/test/'

def pdf_to_image(pdf_path, output_folder, image_format='png'):
    """
    docstring
    """
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        output_image_path = f'{output_folder}/page_{page_num + 1}.{image_format}'
        pix.save(output_image_path)
    
    print('Conversion Complete')

pdf_to_image(pdf_path=SAMPLE_PDF, output_folder=OUTPUT_PATH)