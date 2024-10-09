from card_segment import *
from segment_digit import *
import argparse
# from PIL import Image
import re
import cv2

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
    image_input = args.Read_From_Images

    images = []
    if not image_input:
        if image_saving:
            images = document_reader("test.pdf", image_saving)
    else:
        for i in os.listdir('OutputImages'):
            image_path = os.path.join('OutputImages/', i)
            img = Image.open(image_path)
            images.append(img)

    image_1, image_2, image_3 = initial_segment("test1.jpg")


    easyorc_reader('OutputImages')

    #doctr_reader('OutputImages')

    #keras_predict()

    #keras_orc_predict()


if __name__ == "__main__":
    main()
