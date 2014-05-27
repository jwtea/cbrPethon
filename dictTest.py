import csv

def openCsvDebug(filename):
	data = {}
	data2 = {}
	with open("C:/Python27/pythoncbr/data/"+filename,"rb") as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['Customer ID'] != "":
				key = row['Customer ID']
				data.setdefault(key, [])
				data[key].append(data2['Prod ID'] = row['prodID'])
				data[key].append(data2['Amount'] = row['Amount'])
			if row['Customer ID'] == "":
				data[key].append(row['prodID'])
	return data

orders = openCsvDebug("casesDebug.csv")
print orders