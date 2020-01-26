#!/usr/bin/python3

#Word Processor
#takes input from file?

def word_process(filename):
    """
    (str) -> dict
    """

    #Define Dictionary for product
    product = {"product_name":"", "unit_promo_price":"", "uom":"", "least_unit_for_promo":1, "save_per_unit":"", "discount":"", "organic":0}

    with open("product_dictionary.csv", "r") as f:
        product_names = []
        for row in f:
            row = row.rstrip()
            product_names.append(row)
    #print(product_names)

    with open("units_dictionary.csv", "r") as f:
        units = []
        for row in f:
            row = row.rstrip()
            units.append(row)
    #print(units)

    #open file
    textfile = open(filename, "r")

    #read line by line
    for line in textfile:

        #Strip leading and ending whitespace
        line = line.rstrip()
        line = line.lstrip()

        #if product name is only on one line
        if line in product_names:
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

    
        #if line starts with $
        elif line.startswith("$"):
            
            line = line.lstrip("$")

            #find unit
            for unit in units:
                if unit in line: #add unit to uom
                    product["uom"] = unit

            split_line = line.split("/")
            
            #Determine price
            price = determine_price(split_line[0])
            product["unit_promo_price"] = price

        #if line contains Discount (%) and OFF
        elif "%" in line and "OFF" in line:
            ## Find discount %
            product["discount"] = determine_discount(line)
        
        
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


    #close file
    textfile.close()

    return product

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
    

    print(word_process("test.txt"))




