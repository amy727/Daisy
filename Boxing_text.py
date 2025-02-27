import numpy as np
import cv2

# read the file, convert most of the colored pixels to black
image = cv2.imread('week_4_page_2.jpg')
red_pixels_mask = np.all(image <= [200, 255, 255], axis=-1)  
image[red_pixels_mask] = [0, 0, 0]

# blurs the image and prepares to box
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9,9), 0)
thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
dilate = cv2.dilate(thresh, kernel, iterations=4)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# saves every box into a separate jpg file
ROI_number = 0
for c in cnts:
    area = cv2.contourArea(c)
    if area > 10000:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
        ROI = image[y:y+h, x:x+w]
        cv2.imwrite('ROI_{}.jpg'.format(ROI_number), ROI)
        ROI_number += 1

# cv2.imshow('thresh', thresh)
# cv2.imshow('dilate', dilate)
cv2.imshow('image', image)
cv2.waitKey()

# Code_Modified_From: https://stackoverflow.com/questions/37771263/detect-text-area-in-an-image-using-python-and-opencv
