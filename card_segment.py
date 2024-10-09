# import module
import numpy as np
from pdf2image import convert_from_path
import os
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import random

def document_reader(input_path):

    # Store Pdf with convert_from_path function
    images = convert_from_path(input_path)

    if not os.path.exists('OutputImages'):
        os.mkdir('OutputImages')

    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save(os.path.join('OutputImages','page'+ str(i) +'.jpg'), 'JPEG')
        
    return images

def preprocessing(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    unblur = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=5)

    return dilate, unblur


def initial_segment(image_path, k = 3):
    # Load the image
    print("Starting image processing")
    image = cv2.imread(image_path)
    dilate,unblur = preprocessing(image)

    # Find contours and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    upper_left = []
    height = []
    width = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w/h >= 1 and 900 > w > 60:
            upper_left.append([x,y])
            height.append(h)
            width.append(w)
        else:
            image[y:y + h, x:x + w] = 255
            unblur[y:y + h, x:x + w] = 0


    clusters = cluster_bounding_boxes_kmeans(upper_left, k)

    # Generate random colors for each cluster
    random.seed(42)  # Seed for reproducibility
    cluster_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(k)]

    # Find the bounding box for each cluster
    cluster_boxes = []
    for cluster_id in range(k):
        # Extract the coordinates of all bounding boxes in the cluster
        cluster_coords = [upper_left[idx] for idx in range(len(upper_left)) if clusters[idx] == cluster_id]
        cluster_widths = [width[idx] for idx in range(len(upper_left)) if clusters[idx] == cluster_id]
        cluster_heights = [height[idx] for idx in range(len(upper_left)) if clusters[idx] == cluster_id]

        # Calculate the minimum and maximum x and y to define the big bounding box
        if cluster_coords:
            min_x = min([coord[0] for coord in cluster_coords])
            max_x = max([coord[0] + cluster_widths[idx] for idx, coord in enumerate(cluster_coords)])
            min_y = min([coord[1] for coord in cluster_coords])
            max_y = max([coord[1] + cluster_heights[idx] for idx, coord in enumerate(cluster_coords)])

            # Store the bounding box (min_x, min_y, max_x, max_y)
            cluster_boxes.append((min_x, min_y, max_x, max_y))

            # Draw the bounding box on the image
            cv2.rectangle(image, (min_x, min_y), (max_x, max_y), cluster_colors[cluster_id], 2)

    # Sort cluster boxes by their min_x to maintain order
    cluster_boxes.sort(key=lambda box: box[0])

    # Extract the segments from the original image
    image_1 = unblur[:, cluster_boxes[0][0]:cluster_boxes[0][2]]
    image_2 = unblur[:, cluster_boxes[0][2]:cluster_boxes[1][2]]
    image_3 = unblur[:, cluster_boxes[2][0]:]

    # Display the result (optional, for visualization)
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB))
    plt.title('Segment 1')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB))
    plt.title('Segment 2')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(image_3, cv2.COLOR_BGR2RGB))
    plt.title('Segment 3')
    plt.axis('off')
    plt.show()

    return image_1, image_2, image_3

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

