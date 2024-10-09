import easyocr
# from doctr.models import ocr_predictor
import os
# import keras_ocr
import cv2
#import matplotlib.pyplot as plt


def easyorc_reader(images_path):
    print("easyorc reader")
    # Create an OCR reader object
    reader = easyocr.Reader(['en','hu'])

    img = cv2.imread('OutputImages/page24.jpg')

    # Read text from an image
    result = reader.readtext('OutputImages/page24.jpg', paragraph=True, x_ths=0, width_ths=0, y_ths=0, height_ths=0.0)
    results = {}
    # Print the extracted text

    enlish_world_was_previous = False
    hungarian_world_was_previous = False
    describtion = False
    describtion_end = False

    temp = ""
    for detection in result:
        print(detection[1])
        # if '[' in detection[1]:
        #     print(f"English word: {detection[1]}")
        #     enlish_world_was_previous = True
        #     temp = ""
        # else:
        #     if enlish_world_was_previous:
        #         print(f"Hungarian word: {detection[1]}")
        #         enlish_world_was_previous = False
        #         hungarian_world_was_previous = True
        #     else:
        #         if detection[1][0].isupper():
        #             if '.' in detection[1] or ':' in detection[1] or '?' in detection[1] or '!' in detection[1]:
        #                 temp += ' ' + detection[1]
        #                 print(temp)
        #                 temp=""
        #             else:
        #                 temp += detection[1]
        #         elif '.' in detection[1] or ':' in detection[1] or '?' in detection[1] or '!' in detection[1]:
        #                 temp += ' ' + detection[1]
        #                 print(temp)
        #                 temp=""

    # for img in os.listdir(images_path):
    #     results.append(reader.readtext('OutputImages/' + img))
    # print("\n\n" + "-"*30)
    # result2 = reader.readtext('OutputImages/page24.jpg', paragraph=False)
    # # Print the extracted text
    # for detection in result2:
    #     print(detection[1])



def doctr_reader(images_path):
    print("doctr reader")
    # Load an image
    image_path = 'OutputImages/page24.jpg'

    # Create an OCR predictor
    predictor = ocr_predictor.create_predictor()

    # Perform OCR on the image
    result = predictor(image_path)

    # Print the extracted text
    print(result)

    
    for img in os.listdir(images_path):
        print(img)

def keras_orc_predict():
    import keras_ocr
    import matplotlib.pyplot as plt

    # Create a pipeline for OCR
    pipeline = keras_ocr.pipeline.Pipeline()

    # Load the image
    image = keras_ocr.tools.read('OutputImages/page24.jpg')

    # Perform OCR
    prediction_groups = pipeline.recognize([image])

    # Display results
    for predictions in prediction_groups:
        for text, box in predictions:
            print(f'Detected text: {text}')
            # Draw bounding box
            #keras_ocr.tools.drawBoxes(image, [box], color='red')

    # Show the image with detected text
    plt.imshow(image)
    plt.axis('off')
    plt.show()
