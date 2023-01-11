import csv

def item_extract()
    res = []
    with open('./items.csv',newline = '') as file:
        reader = csv.reader(file)
        for row in reader:
    	    res.append(row[0])
    return res
