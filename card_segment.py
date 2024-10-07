# import module
import numpy as np
from pdf2image import convert_from_path
import os
import cv2
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image
from sklearn.cluster import DBSCAN
from skimage import io

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

def preprocessing(input_img):
    # Load image in grayscale
    image = cv2.imread(input_img, cv2.IMREAD_GRAYSCALE)

    # Threshold the image to binary (black and white) using adaptive thresholding
    binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY, 11, 2)

    return binary_image


def optics_segment(image_path):
    # Load the image
    print("Starting image processing")

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 6))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    upper_left = []
    height = []
    width = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w/h >= 1:
            cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
            upper_left.append([x,y])
            height.append(h)
            width.append(w)

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    return upper_left, height, width

