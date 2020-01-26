import numpy as np
import cv2
from PIL import Image
import pytesseract
import glob

def process_text(image_name):
    '''
    ('string') -> string
    Processes all the text in a given file to a string in csv format
    '''
    image = cv2.imread(image_name)
    color_pixels_mask = np.all(image <= [200, 255, 255], axis = -1)
    image[color_pixels_mask] = [0, 0, 0]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilate = cv2.dilate(thresh, kernel, iterations = 4)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    
    ROI_number = 0

    # the text to be written into the .csv file
    image_name_text = ''

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 10000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
            ROI = image[y:y+h, x:x+w]

            # create a file for one box
            cv2.imwrite('ROI.jpg', ROI)

            # read the text in the box
            p_text = ocr_core('ROI.jpg')

            # process the text
            image_name = image_name.split('.')
            image_name_text += image_name[0] + ','
            image_name_text += word_process(p_text)

            ROI_number += 1
    
    return image_name_text

    
# reads the text in the box
def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text

def word_process(product_text):
    pass

if __name__ == '__main__':  
    product_text = 'flyer_name,product_name,unit_promo_price,uom,least_unit_for_promo,save_per_unit,discount,organic\n'  
    for file_name in glob.iglob(r'C:\Users\admin\*.jpg'):
        product_text += process_text(file_name)
    
    output_file = open('output.csv', 'w')
    output_file.write(product_text)
    output_file.close()



# Code_Modified_From: 
# https://stackoverflow.com/questions/37771263/detect-text-area-in-an-image-using-python-and-opencv
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html