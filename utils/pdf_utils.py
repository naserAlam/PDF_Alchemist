import fitz
import os

def pdf_to_images(pdf_path, output_folder, file_name='test', image_format='png'):
    """
    docstring
    """
    pdf_document = fitz.open(pdf_path)
    total_pages = len(pdf_document)
    image_paths = []

    file_name_without_ext = os.path.splitext(file_name)[0]
    subfolder_path = os.path.join(output_folder, file_name_without_ext)
    os.makedirs(subfolder_path, exist_ok=True)
    print(subfolder_path + '\n')

    for page_num in range(total_pages):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        output_image_path = os.path.join(subfolder_path, f'page_{page_num + 1}.{image_format}')
        pix.save(output_image_path)
        print(f"Saved image: {output_image_path}") 
        image_paths.append(output_image_path)

    return image_paths