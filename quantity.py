import fileOps,math
products = fileOps.openCsv("products.csv")
orders = fileOps.openCsv1("cases.csv")
print type(orders)
customerProducts = []
similarOrders = {}
custID = raw_input('__Enter customer ID:')
 
#Iterate over the CSV. 
for key, prods in orders.iteritems():
 
	if "c" + custID == key:
		
		#Once we've find the customer, we've got our list of products and can break the loop.
		customerProducts = prods
 
print '----------'
 
for key, prods in orders.iteritems():
 
	if custID != key:
		customerProducts = set(customerProducts)
		prods = set(prods)
 
		extraProducts = prods ^ customerProducts	#Xor
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
			similarOrders[key] = sim 
 
 
print "-----"
print "Summary for customer c" + custID
print "Number of similar orders: " + str(len(similarOrders))
 
for key, order in similarOrders.iteritems():
	print "similarOrders["+key+"] = " + str(order)