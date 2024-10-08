# import module
# from pdf2image import convert_from_path
import os

def document_reader(input_path, save_images):

    # Store Pdf with convert_from_path function
    images = convert_from_path(input_path)

    if not os.path.exists('OutputImages'):
        os.mkdir('OutputImages')

    if save_images:
        for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save(os.path.join('OutputImages','page'+ str(i) +'.jpg'), 'JPEG')
        
    return images