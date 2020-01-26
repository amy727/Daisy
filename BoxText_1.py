import cv2
import numpy as np

image = cv2.imread('week_1_page_2.jpg')

# Convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_red = np.array([170,120,70])
upper_red = np.array([180,255,255])

# Threshold the HSV image to get only red colors
mask1 = cv2.inRange(hsv, lower_red, upper_red)

lower_black = np.array([0,0,0])
upper_black = np.array([180, 255, 80])

# Threshold the HSV image to get only black colors
mask2 = cv2.inRange(hsv, lower_black, upper_black)

mask3 = mask1 + mask2
cv2.imshow('mask1', mask1)
cv2.imshow('mask2', mask2)
cv2.imshow('mask3', mask3)

# Bitwise-AND mask and original image
# mask = cv2.bitwise_and(image, image, mask = mask3)

# gray = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
#cv2.imshow('gray', gray)

blur = cv2.GaussianBlur(mask3, (9,9), 0)
cv2.imshow('blur', blur)

#thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
#cv2.imshow('kernel', kernel)
dilate = cv2.dilate(blur, kernel, iterations=4)
#cv2.imshow('dilate', dilate)
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
'''
ROI_number = 0
for c in cnts:
    area = cv2.contourArea(c)
    if area > 10000:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
        ROI = image[y:y+h, x:x+w]
        cv2.imwrite('ROI_{}.jpg'.format(ROI_number), ROI)
        ROI_number += 1
'''
cv2.imshow('image', image)
cv2.waitKey()
