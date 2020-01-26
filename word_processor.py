#!/usr/bin/python3

#Word Processor
#takes input from file?

def word_process(text):
    """
    (str) -> str
    Output string format: "product_name,unit_promo_price,uom,least_unit_for_promo,save_per_unit,discount,organic\n"
    """

    #Define Dictionary for product
    product = {"product_name":"", "unit_promo_price":"", "uom":"", "least_unit_for_promo":1, "save_per_unit":"", "discount":"", "organic":0}

    #split text file
    textlines = text.split("\n")

    print(textlines)
    if len(textlines) < 3:
        return

    #Define list of product names
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
        if i < len(textlines)-2:
            nextline = textlines[i+1]

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



if __name__ == "__main__":
    
    f = open("test.txt", "r")
    read = f.read()
    print(word_process(read))





