import fileOps,math

from simMetrics import *
from collections import defaultdict
products = fileOps.openCsv("products.csv")
orders = fileOps.openCsvDebug("cases.csv")
orderDebug = fileOps.openCsvDebug("casesDebug.csv")
newOrderDict = {}
customerProducts = []
orderSimilarity = {}
#similarityThreshold = raw_input('Enter threshold:')
similarityThreshold = 0.3 
custID = raw_input('Enter customer ID:')
#Iterate over the CSV. 
for key, prods in orders.iteritems():
 
	if "c" + custID == key:
		
		#Once we've find the customer, we've got our list of products and can break the loop.
		customerProducts = prods
		print customerProducts
 
print '----------'

for key, prods in orders.iteritems():
 
	if custID != key:
		customerProducts = set(customerProducts)
		prods = set(prods)
 
		extraProducts = customerProducts ^ prods	#Xor
		extraProducts = prods & extraProducts
 		similarProducts = prods & customerProducts	#interseciton
		#Output
		print ""
		print "Checking customer " + str(key)
		print "  Number of extra products: " + str(len(extraProducts))		
		print "  Number of similar products: " + str(len(similarProducts))
 
		if(len(similarProducts)!= 0 and len(extraProducts)):
			temp1 = len(similarProducts)*len(similarProducts)
			temp2 = len(prods)*len(prods)
			sim = math.sqrt(float(temp1)/float(temp2))
			orderSimilarity[key] = sim 
 
print "-----"
print "Summary for customer c" + custID
print "Number of similar orders: " + str(len(orderSimilarity))
print "-----"

mostSimOrder = 0
for key, sim in orderSimilarity.iteritems():
	if sim > mostSimOrder:
		mostSimOrder = sim
	keyToSearch = key

	#if sim > 0.25:
		#keyToSearch = key
		#moved out of order sim loop to only use most similar result
print "Most Similar order is ["+key+"] = " + str(sim)
print "-------"
#print "probability of wanting the extra item:"

for key, prods in orders.iteritems():
	if key == keyToSearch:
		prods = set(prods)
		extraProducts = prods ^ customerProducts
		extraProducts = prods & extraProducts
		print "Extra Products " + str(extraProducts)
		similarProducts = prods & customerProducts
		if len(extraProducts) != 0:
		
			for extraProd in extraProducts:
				extraProdCat = fileOps.getProductCat(extraProd)
				extraProdSim = 0

				for simProd in similarProducts:
					simProdCat = fileOps.getProductCat(simProd)
					extraProdSim += category[simProdCat][extraProdCat]

				extraProdSim = extraProdSim / len(similarProducts)
				print "sim for :" + extraProd + ":"+ str(extraProdSim)
				if extraProdSim > 0.25:
					key = "n1"
					newOrderDict.setdefault(key, [])
					newOrderDict[key].append(extraProd)
					#print "_______________"
					#print newOrderDict
print "========="
print "Suggesting new order of:"+str(newOrderDict['n1'])
status = raw_input('Order Ok ?:')
if status == 'y':
	print "Writing new order to file"
	print "-------------------------"
	fileOps.writeRecord(newOrderDict)
if status == 'e':
	finishEdit = 1
	while finishEdit ==1:
		print "-----"
		remove = raw_input('Type product to remove from order:')
		print "-----"
		updatedOrder = {}
		for key, values in newOrderDict.items():
			updatedOrder.setdefault(key, [])
		        for value in values:
		            if value != remove:
		            		updatedOrder[key].append(value)
		newOrderDict = updatedOrder
		print "updated Order:"+str(newOrderDict)
		print "-----"
		if(raw_input('Are you finished?') == 'y'):
			print "-----"
			finishEdit = 0
			fileOps.writeRecord(newOrderDict)



# suggest the sim products 
# save to new order 


