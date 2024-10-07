from card_segment import * 
from segment_digit import *
import argparse

def parser():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Process Image_saving argument.")

    # Add the argument for Image_saving
    parser.add_argument('--Image_saving', type=lambda x: (str(x).lower() == 'true'), 
                        help="A flag to enable or disable image saving", 
                        default=False)
    parser.add_argument('--Read_From_Images', type=lambda x: (str(x).lower() == 'true'), 
                        help="A flag to enable or disable using images as an input", 
                        default=False)

    # Parse the arguments
    args = parser.parse_args()
    return args

def main():

    # Access the Image_saving value
    args = parser()
    image_saving = args.Image_saving

    images = document_reader("test.pdf", image_saving)

    import pytesseract
    from PIL import Image
    import re

    # Load the image from the file path
    #image_path = '/mnt/data/page10.jpg'
    #img = Image.open(image_path)

    # Perform OCR to extract the text
    text = pytesseract.image_to_string(images, lang='eng+hun')

    # Function to extract English word, Hungarian word, and description
    def extract_information(text):
        # Splitting the text into lines
        lines = text.split("\n")
        data = []
         
        for line in lines:
            print(line)
            # Using regex to capture the pattern
            # Assumes format: [english_word] [IPA/pronunciation] [number] [hungarian_word] [description]
            match = re.match(r"(\w+)\s+\[\S+\]\s+\d+\s+(\w+),?\s+(.+)", line)
            if match:
                english_word = match.group(1)
                hungarian_word = match.group(2)
                description = match.group(3)
                data.append((english_word, hungarian_word, description))
        
        return data

    # Extract information from the OCR result
    extracted_data = extract_information(text)

    # Print the results
    for entry in extracted_data:
        print(f"English Word: {entry[0]}, Hungarian Word: {entry[1]}, Description: {entry[2]}")




if __name__ == "__main__":
    main()
