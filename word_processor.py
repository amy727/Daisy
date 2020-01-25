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
    print(product_names)

    with open("units_dictionary.csv", "r") as f:
        units = []
        for row in f:
            row = row.rstrip()
            units.append(row)
    print(units)

    #open file
    textfile = open(filename, "r")

    #read line by line
    for line in textfile:

        #Strip leading and ending whitespace
        line = line.rstrip()
        line = line.lstrip()

        if line in product_names:
            product["product_name"] = line
    

    textfile.close()

    return product

if __name__ == "__main__":
    

    print(word_process("test.txt"))




