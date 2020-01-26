#%%
import numpy as np
import cv2
from PIL import Image
import pytesseract
from glob import glob

#pytesseract.pytesseract.tesseract_cmd = r'/Users/jorrynlu/anaconda3/lib/python3.7/site-packages/tesseract'

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
    i_name = image_name.split('/')
    flyer_name = i_name[-1][:-4] + ','

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
            if word_process(p_text) != None:
                image_name_text += flyer_name + word_process(p_text)

            ROI_number += 1
    
    return image_name_text

    
# reads the text in the box
def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text

def word_process(product_text):
    """
    (str) -> str
    Output string format: "product_name,unit_promo_price,uom,least_unit_for_promo,save_per_unit,discount,organic\n"
    """

    # Define Dictionary for product
    product = {"product_name":"", "unit_promo_price":"", "uom":"", "least_unit_for_promo":1, "save_per_unit":"", "discount":"", "organic":0}

    # split text file
    textlines = product_text.split("\n")

    
    if len(textlines) < 3:
        return None
    
    for line in textlines:
        if line == '' or line == ' ':
            textlines.remove(line)
    print(textlines)

    # Define list of product names
    with open("product_dictionary.csv", "r") as f:
        product_names = []
        for row in f:
            row = row.rstrip()
            product_names.append(row)
    #print(product_names)

    #Define list of units
    with open("units_dictionary.csv", "r") as f:
        units = []
        for row in f:
            row = row.rstrip()
            units.append(row)
    #print(units)


    #read line by line
    for i in range(len(textlines)):
        #Define line and nextline
        line = textlines[i]
        if i < len(textlines) - 2:
            nextline = textlines[i + 1]
        else:
            nextline = ''
            

        #Strip leading and ending whitespace
        line = line.rstrip()
        line = line.lstrip()
        nextline = nextline.rstrip()
        nextline = nextline.lstrip()

        #tries to match product name
        #print(line+" "+nextline)
        if (line+" "+nextline) in product_names:
            if product["product_name"] == "":
                product["product_name"] = (line+" "+nextline)

        if line in product_names:
            if product["product_name"] == "":
                product["product_name"] = line

        ## CASE 1
        #if line starts with SAVE
        elif line.startswith("SAVE"):
            
            ## CASE 1.1 - Save per unit
            #split line by $ sign
            if "$" in line:
                
                #Ex: SAVE $2.99 on 2
                if "on" in line:
                    split_line = line.split("on")
                    product["save_per_unit"] = determine_price(split_line[0])
                    try:
                        product["least_unit_for_promo"] = int(split_line[1])                    
                    except:
                        pass
                
                #Only price saving info
                else:
                    product["save_per_unit"] = determine_price(line)

            ## CASE 1.2 - Save per discount (ie SAVE 20%)
            elif "%" in line:
                split_line = line.split("%")
                discount = determine_discount(split_line[0])
                product["discount"] = discount

            ##ie SAVE $3.99 per pound
            for unit in units:
                if unit in line: #add unit to uom
                    product["uom"] = unit

    
        #if line starts with $
        elif line.startswith("$"):

            #find unit
            for unit in units:
                if unit in line: #add unit to uom
                    product["uom"] = unit

            split_line = line.split("/")
            
            #Determine price
            price = determine_price(split_line[0])
            product["unit_promo_price"] = price

            ##ie $3.99 per pound
            for unit in units:
                if unit in line: #add unit to uom
                    product["uom"] = unit

        #if line contains Discount (%) and OFF
        elif "%" in line and "OFF" in line:
            ## Find discount %
            product["discount"] = determine_discount(line)

        elif "HALF" in line and "OFF" in line:
            product["discount"] = 0.5
        
        #if the line starts with a digit
        elif len(line)>0 and line[0].isdigit():

            #least units/$price format
            if "/" in line:
                split_line = line.split("/")
                try:
                    product["least_unit_for_promo"] = int(split_line[0])
                except:
                    pass

                split_line[1] = split_line[1].lstrip("$")
                price = determine_price(split_line[1])
                product["unit_promo_price"] = price

            ##OR could be (7 oz.)
            for unit in units:
                if unit in line: #add unit to uom
                    product["uom"] = line

        #If product is organic
        if "organic" in line:
            product["organic"] = 1

        
    ##Make sure everything is in UNIT of 1
    if product["least_unit_for_promo"] > 1:
        unit_num = product["least_unit_for_promo"]
        unit_price = product["unit_promo_price"]
        unit_save = product["save_per_unit"]
        #print(unit_num, unit_price, unit_save)

        if product["unit_promo_price"] != "":
            product["unit_promo_price"] = float(unit_price)/unit_num
        if product["save_per_unit"] != "":
            product["save_per_unit"] = float(unit_save)/unit_num 
    
    if product["product_name"] == '':
        return None
    
    output = (product["product_name"] + "," \
        + str(product["unit_promo_price"]) + "," \
        + product["uom"] + "," \
        + str(product["least_unit_for_promo"]) + ","\
        + str(product["save_per_unit"]) + "," \
        + str(product["discount"]) + "," \
        + str(product["organic"]) + "\n") 
    
    return output

def determine_price(str_price):
    """
    (str) -> num
    """

    price = 0.0

    #Removes non-digit characters
    for ch in str_price:
        if not ch.isdigit():
            str_price = str_price.replace(ch, "")

    #dollars and cents
    if len(str_price) >= 3:
        try:
            price = float(str_price)/100
        except:
            pass
    
    #probably in cents
    elif len(str_price) == 2 and str_price[0] in "987":
        try:
            price = float(str_price)/100
        except:
            pass

    #probably just dollars
    else:
        try:
            price = float(str_price)
        except:
            pass

    return price


def determine_discount(str_discount):
    """
    (str) -> num
    """
    discount = 0

    #Removes non-digit characters
    for ch in str_discount:
        if not ch.isdigit():
            str_discount = str_discount.replace(ch, "")

    #Calculates discount
    try:
        discount = float(str_discount)/100
    except:
        pass
    
    return discount


if __name__ == '__main__':  
    product_text = 'flyer_name,product_name,unit_promo_price,uom,least_unit_for_promo,save_per_unit,discount,organic\n'  
    files = sorted(glob(r'/Users/jorrynlu/Desktop/flyer_image/*.jpg'))
    for file_name in files:
        product_text += process_text(file_name)
    
    output_file = open('output.csv', 'w')
    output_file.write(product_text)
    output_file.close()



# Code_Modified_From: 
# https://stackoverflow.com/questions/37771263/detect-text-area-in-an-image-using-python-and-opencv
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html