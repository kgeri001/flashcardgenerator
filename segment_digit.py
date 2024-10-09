import easyocr
import os
import cv2
import matplotlib.pyplot as plt


class Own_dictionary:
    def __init__(self, english_word, hungarian_word, description, box_point):
        self.english_word = english_word
        self.hungarian_word = hungarian_word
        self.description = description
        self.box_point = box_point

    def to_dict(self):
        # Convert the node structure to a dictionary for JSON conversion
        return {
            "english_word": self.english_word,  
            "hungarian_word": self.hungarian_word,
            "description": self.description
        }


def easyocr_reader(image_1):
    #print("easyocr reader")
    # Create an OCR reader object
    reader = easyocr.Reader(['en','hu'])

    result = reader.readtext(image_1)#, paragraph=True, x_ths=0, width_ths=0, y_ths=0, height_ths=0.0)
    temp = ""
    results = []
    first = True
    temp_box = []
    for detection in result:
        #print(detection[1])
        bbox, text, confidance = detection
        temp += text
        if detection[1][-1].isnumeric():
            word_end = -1
            for i, char in enumerate(temp):
                if not char.isalpha() and word_end == -1:
                    word_end = i
            if first:
                results.append(Own_dictionary(english_word=temp[0:word_end], box_point=bbox, hungarian_word="", description=""))
            else:
                results.append(Own_dictionary(english_word=temp[0:word_end], box_point=temp_box, hungarian_word="", description=""))
                temp_box = []
            temp = ""
            first = True
        else:
            first = False
            if len(temp_box) == 0:
                temp_box = bbox

    #for item in results:
        #print(item.english_word, item.box_point)

    # for detection in result:
    #     bbox, text, confidance = detection
         #print(bbox, confidance)

    # for item in results:
    #     bbox = item.box_point
    #     cv2.rectangle(image_1, (bbox[0]), (bbox[2]), (255, 255, 255), 2)
        
    # plt.figure(figsize=(15, 5))
    # plt.imshow(cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB))
    #plt.show()
    return results
