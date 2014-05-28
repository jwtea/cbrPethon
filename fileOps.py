import csv
#new
from collections import defaultdict
def openCsv1(filename):
	data=defaultdict(list)
	with open("C:/Python27/pythoncbr/data/"+filename,"rb") as data_file:
		reader=csv.DictReader(data_file)
		for row in reader:
			if row['Customer ID']!= "":
				data[row['Customer ID']].append(row['prodID'])
	return data
def openCsvDebug(filename):
	data = {}
	with open("C:/Python27/pythoncbr/data/"+filename,"rb") as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['Customer ID'] != "":
				key = row['Customer ID']
				data.setdefault(key, [])
				data[key].append(row['prodID'])
			if row['Customer ID'] == "":
				data[key].append(row['prodID'])
	return data
def openCsvDebugAmount(filename):
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
def getStockistType(ID):
	data = {}
	with open("C:/Python27/pythoncbr/data/casesDebug.csv","rb") as f:
		reader = csv.DictReader(f,delimiter = ",")
		for row in reader:
			if row['Customer ID'] != "":
				if ID == row['Customer ID']:
					data=row['Stockist Type']
	return data
def getProductCat(prodID):
	with open("C:/Python27/pythoncbr/data/products.csv","rb") as f:
		reader = csv.DictReader(f,delimiter = ",")
		for row in reader:
			if prodID == row['prodID']:
				return row['Category']
def getProductInfo(prodID):
	data = {}
	with open("C:/Python27/pythoncbr/data/products.csv","rb") as f:
		reader = csv.DictReader(f,delimiter = ",")
		for row in reader:
			if prodID == row['prodID']:
				data['Name']=(row['Product Name'])
				data['Category']=(row['Category'])
				data['Size']=(row['Size'])
				data['Price']=(row['Price'])
		return data
def openCsv(filename):
	products = []
	with open("C:/Python27/pythoncbr/data/"+filename,"rb") as f:
		reader = csv.DictReader(f,delimiter = ",")
		for row in reader:
			products.append(row)
	return products
def writeCsv(data):
	print "in write"
	with open("C:/Python27/pythoncbr/data/testnew.csv","wb") as f:
		colNames = data[0].keys()
		writer = csv.DictWriter(f,delimiter = ",",fieldnames=colNames)
		writer.writeheader()
		for line in data:
			writer.writerow(line)
def getNextOrderID():
	data = ""
	with open("C:/Python27/pythoncbr/data/casesDebug.csv","rb") as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['Order ID']!= "":
				data = row['Order ID']
				print data
	return data
def writeRecordQuant(data,temp,stockistType):
	with open('C:/Python27/pythoncbr/data/casesDebug.csv', 'a') as f:
	    writer = csv.writer(f,lineterminator='\n')
	    for key, values in data.items():
	    	for value in values[0:1]:
	       	 	writer.writerow([temp,key, value[0],value[1],stockistType])
	        for value in values[1:]:
	            writer.writerow([None,None, value[0],value[1]])	
def writeRecord(data,temp):
	with open('C:/Python27/pythoncbr/data/casesDebug.csv', 'a') as f:
	    writer = csv.writer(f,lineterminator='\n')
	    for key, values in data.items():
	        writer.writerow([temp,key, values[0]])
	        for value in values[1:]:
	            writer.writerow([None,None, value])