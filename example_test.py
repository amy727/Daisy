#!/usr/bin/python3
from PIL import Image
import pytesseract

def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text


if __name__ == "__main__":

    filename = "./flyer_images/week_1_page_1.jpg"
    print(ocr_core(filename))
