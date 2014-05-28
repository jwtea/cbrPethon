import csv
#new
from collections import defaultdict
def openCsvDebug(filename):
	data = {}
	with open("C:/Python27/pythoncbr/data/"+filename,"rb") as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['Customer ID'] != "":
				key = row['Customer ID']
				temp = [row['prodID'],row['Amount']]
				data.setdefault(key, [])
				data[key].append(temp)
			if row['Customer ID'] == "":
				temp = [row['prodID'],row['Amount']]
				data[key].append(temp)
	return data
def writeRecord(data,temp):
	with open('C:/Python27/pythoncbr/data/casesDebug.csv', 'a') as f:
	    writer = csv.writer(f,lineterminator='\n')
	    for key, values in data.items():
	        writer.writerow([temp,key, values[0]])
	        for value in values[1:]:
	            writer.writerow([None,None, value])
orders = openCsvDebug("casesDebug.csv")
customerProducts = []
custID = "1"
for key, prods in orders.iteritems():
	if "c" + custID == key:
		for prod in prods:
			print prod[0]
	#Once we've find the customer, we've got our list of products and can break the loop.
			customerProducts.append(prod[0])
			print customerProducts
