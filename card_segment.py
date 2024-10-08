# import module
import numpy as np
from pdf2image import convert_from_path
import os
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import random

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


def optics_segment(image_path, k = 3):
    # Load the image
    print("Starting image processing")

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=5)

    # Find contours and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    upper_left = []
    height = []
    width = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w/h >= 1:
            upper_left.append([x,y])
            height.append(h)
            width.append(w)

    clusters = cluster_bounding_boxes_kmeans(upper_left, k)

    # Generate random colors for each cluster
    random.seed(42)  # Seed for reproducibility
    cluster_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(k)]

    # Draw the bounding boxes with their respective cluster colors
    for idx, (coord, h, w) in enumerate(zip(upper_left, height, width)):
        cluster_id = clusters[idx]
        color = cluster_colors[cluster_id]
        x, y = coord
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

    # Display the result
    plt.figure(figsize=(10, 8))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

def cluster_bounding_boxes_kmeans(upper_left, k=3):
    """
    Clusters the bounding boxes using the KMeans algorithm based on their x-coordinate.

    Parameters:
    - upper_left: List of [x, y] coordinates of the upper left corners of bounding boxes.
    - k: Number of clusters to create.

    Returns:
    - clusters: A list where each element corresponds to the cluster assignment of each bounding box.
    """
    # Extract the x-coordinates of the bounding boxes
    x_coords = np.array([coord[0] for coord in upper_left]).reshape(-1, 1)

    # Create and fit the KMeans model
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(x_coords)

    # Get the cluster assignments for each bounding box
    clusters = kmeans.labels_

    return clusters

