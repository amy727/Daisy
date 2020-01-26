#!/usr/bin/python3

#Word Processor
#takes input from file?

def word_process(filename):

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

        #if line starts with SAVE
        elif line.startswith("SAVE"):
            #split line by $ sign
            split_line = line.split("$")
            #print(split_line)
            amt_saved = ""
            
            #check if character is numeric
            for ch in split_line[1]:
                try:
                    int(ch)
                    amt_saved = amt_saved + ch
                    print(amt_saved)
                except:
                    break #break from loop
            
            product["save_per_unit"] = amt_saved
    
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

        #if the line starts with a digit
        elif len(line)>0 and line[0].isdigit():

            #least units/$price format

            split_line = line.split("/")
            product["least_unit_for_promo"] = int(split_line[0])

            split_line[1] = split_line[1].lstrip("$")
            price = determine_price(split_line[1])
            product["unit_promo_price"] = price

        #if line contains Discount (%)
        elif "%" in line:
            if "OFF" in line:
                ## Find discount %
                split_line = line.split("%")
                
                #Remove non digits
                for ch in split_line[0]:
                    if not ch.isdigit():
                        split_line[0] = split_line[0].replace(ch, "")

                #Calculates discount
                discount = float(split_line[0])/100

                product["discount"] = discount


    #close file
    textfile.close()

    return product

def determine_price(str_price):
    """
    (str) -> num
    """

    for ch in str_price:
        if not ch.isdigit():
            str_price = str_price.replace(ch, "")

    if len(str_price) >= 3:
        try:
            price = float(str_price)/100
        except:
            pass
        
    else:
        try:
            price = float(str_price)
        except:
            pass

    return price

if __name__ == "__main__":
    

    print(word_process("test.txt"))




