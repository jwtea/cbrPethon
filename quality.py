import fileOps
from collections import OrderedDict
from operator import itemgetter
from simMetrics import *
orders = fileOps.openCsv("test.csv")

def categoryMet(cat):
	temp = {}
	for item in category[cat].items():
		temp[item[0]] = item[1]
	ordTemp = OrderedDict(sorted(temp.items(),key = itemgetter(1),reverse=True))
	return ordTemp

def stockistMet(sType):
	temp = {}

	for item in stockist[sType].items():
		temp[item[0]] = item[1]

	ordTemp = OrderedDict(sorted(temp.items(),key = itemgetter(1),reverse=True))
	return ordTemp

custID = raw_input('Enter Customer ID:')
print 'Customer:'+custID
for ords in orders:

	if ords['Customer ID'] == custID:
		print ords['Order ID'],
orderID = int(raw_input(':')) 
print '----------'
#define metrics

catMet = categoryMet(orders[orderID-1]['Category'])
stockMet = stockistMet(orders[orderID-1]['Stockist Type'])
simOrd = []

#find similarity
for ords in orders:

	if int(ords['Order ID']) != orderID:
		catSim = catMet[ords['Category']] * categoryWeight
		stockSim = stockMet[ords['Stockist Type']] * stockistWeight
		globalSim = (catSim + stockSim) / totalWeight
		print ords['Order ID'],stockSim
		simOrd.append([ords['Order ID'],ords['Customer ID'],globalSim])

simOrd = sorted(simOrd,key=lambda ord: ord[2], reverse = True)
simOrd = simOrd [:5]

for i in simOrd:

	for ords in orders:

		if ords['Order ID'] == i[0] and ords['Customer ID'] == i[1]:
			print "Most similar order to a factor of:"+str(i[2])+": is Order:", ords['Order ID']