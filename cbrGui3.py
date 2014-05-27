import fileOps,math
from Tkinter import *
from simMetrics import *
from collections import defaultdict
products = fileOps.openCsv("products.csv")
orders = fileOps.openCsvDebug("casesDebug.csv")
orderDebug = fileOps.openCsvDebug("casesDebug.csv")
newOrderDict = {}
customerProducts = []
orderSimilarity = {}
similarityThreshold = 0.3
#similarityThreshold = raw_input('Enter threshold:')
state = 1

#Iterate over the CSV. 
def main():
	forgetFrames()
	global newOrderDict
	newOrderDict = {}
	customerProducts = []
	orderSimilarity = {}
	 
	custID = custEntry.get()
	print '++=========++' 
	for key, prods in orders.iteritems():
		if "c" + custID == key:
			#Once we've find the customer, we've got our list of products and can break the loop.
			customerProducts += prods
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
	#text.insert(INSERT,"Summary for customer c"+custID)
	#text.insert(END,"-----")
	summaryLabelVar.set("Summary for customer c" + custID)
	summaryLabelVar2.set("Number of similar orders: " + str(len(orderSimilarity)))
	mostSimOrder = 0
	for key, sim in orderSimilarity.iteritems():
		if sim > mostSimOrder:
			mostSimOrder = sim
		keyToSearch = key
	summaryLabelVar3.set("The most Similar order is ["+key+"] = " + str(sim))
	#print "probability of wanting the extra item:"
	for key, prods in orders.iteritems():
		if key == keyToSearch:
			prods = set(prods)
			extraProducts = prods ^ customerProducts
			extraProducts = prods & extraProducts
			print "Extra Products " + str(extraProducts)
			similarProducts = prods & customerProducts
			if len(extraProducts) != 0:
				if v.get() == 0:
					for extraProd in extraProducts:
						extraProdCat = fileOps.getProductCat(extraProd)
						extraProdSim = 0

						for simProd in similarProducts:
							simProdCat = fileOps.getProductCat(simProd)
							extraProdSim += category[simProdCat][extraProdCat]

						extraProdSim = extraProdSim / len(similarProducts)
						print "sim for :" + extraProd + ":"+ str(extraProdSim)
						if extraProdSim > similarityThreshold:
							newOrderDict.setdefault("c"+custID, [])
							newOrderDict["c"+custID].append(extraProd)
							#print "_______________"
							#print newOrderDict
				else:
					for extraProd in extraProducts:
						newOrderDict.setdefault("c"+custID, [])
						newOrderDict["c"+custID].append(extraProd)

	print "========="
	suggestLabelVar.set("Suggesting new order of:"+str(newOrderDict))
	suggestLabelVar2.set("Order Ok ?:")
	summaryFrame.pack()
	ordOptionsFrame.pack()
	
	# suggest the sim products 
	# save to new order
def forgetFrames():
	summaryFrame.pack_forget()
	ordOptionsFrame.pack_forget()
	editFrame.pack_forget()
def writeOrd():
	print "Writing new order to file"
	print "-------------------------"
	print newOrderDict
	temp = int(fileOps.getNextOrderID())
	temp = str(temp+1)
	fileOps.writeRecord(newOrderDict,temp)
	summaryLabelVar.set("New Order Saved")
	newCustProductsVar.set("")
	if(state == 0):
		addOrder()
	if(state == 1):
		showMain()
def addProd():
	global newOrderDict
	print str(newOrderDict)
	present = False
	updatedOrder = {}
	add = eVar.get()
	print add
	for key, values in newOrderDict.items():
		updatedOrder.setdefault(key, [])
	        for value in values:
	            updatedOrder[key].append(value)
	            if value == add:
	            	present = True
	        if present != True:
	        	updatedOrder[key].append(add)
	newOrderDict = updatedOrder
	suggestLabelVar.set("Suggesting new order of:"+str(newOrderDict))
	newCustProductsVar.set(str(newOrderDict))
	print newOrderDict

def removeProd():
	global newOrderDict
	print "newOrder"+str(newOrderDict)
	remove = eVar.get()
	updatedOrder = {}
	for key, values in newOrderDict.items():
		updatedOrder.setdefault(key, [])
	        for value in values:
	            if value != remove:
	            		updatedOrder[key].append(value)
	newOrderDict = updatedOrder
	suggestLabelVar.set("Suggesting new order of:"+str(newOrderDict))
	newCustProductsVar.set(str(newOrderDict))
	print "-----"
def editOrd():
	removeLabelVar.set("Enter products to edit")
	editFrame.pack()
def setSim():
	similarityThreshold = similarityOptionVar.get()
	print "sim changed "+ str(similarityThreshold)
def getNextCustID():
	orders = fileOps.openCsvDebug("casesDebug.csv")
	temp = 0
	for key, prods in orders.iteritems():
		if int(key[1:]) > temp:
			temp = int(key[1:])
	temp = temp + 1
	temp = 'c' + str(temp)
	return temp
def lookUpProduct():
	productInfo = fileOps.getProductInfo(prodLvar.get())
	print productInfo
	prodName.set("Name:"+productInfo['Name'])
	prodCat.set("Category:"+productInfo['Category'])
	prodPrice.set("Price:"+productInfo['Price'])
	prodSize.set("Size:"+productInfo['Size'])

#states
def addOrder():
	global newOrderDict
	global state
	state = 0 
	newOrderFrame.pack()
	configureFrame.pack_forget()
	radioFrame.pack_forget()
	mainFrame.pack_forget()
	summaryFrame.pack_forget()
	ordOptionsFrame.pack_forget()
	editFrame.pack_forget()
	productLookupFrame.pack(side=BOTTOM)
	productLookupResults.pack(side=BOTTOM)

	newCustIdVar.set("New Customer Order :"+getNextCustID())
	key = getNextCustID()
	newOrderDict = {}
	newOrderDict.setdefault(key, [])
	print str(newOrderDict)

def showOptions():
	print v.get()
	newOrderFrame.pack_forget()
	configureFrame.pack()
	radioFrame.pack()
	mainFrame.pack_forget()
	summaryFrame.pack_forget()
	ordOptionsFrame.pack_forget()
	editFrame.pack_forget()
	productLookupFrame.pack_forget()
	productLookupResults.pack_forget()

def showMain():
	global state
	state = 1
	newOrderFrame.pack_forget()
	configureFrame.pack_forget()
	radioFrame.pack_forget()
	mainFrame.pack()
	summaryFrame.pack_forget()
	ordOptionsFrame.pack_forget()
	editFrame.pack_forget()
	productLookupFrame.pack(side=BOTTOM)
	productLookupResults.pack(side=BOTTOM)
#Setup Gui
cbrGui = Tk()
cbrGui.title("Python CBR")
cbrGui.geometry("500x500")
#Setup Menu
menubar = Menu(cbrGui)
cbrGui.config(menu=menubar)
optionsMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Options", menu = optionsMenu)
optionsMenu.add_command(label = "Add new order",command=addOrder)
optionsMenu.add_command(label = "Suggest new order",command=showMain)
optionsMenu.add_command(label = "View orders",command=forgetFrames)
optionsMenu.add_separator()
optionsMenu.add_command(label = "Configure",command=showOptions)
#Add order frame 
newCustIdVar = StringVar() #get the last var 
newCustProductsVar = StringVar()
#Configure
v = IntVar()
v1 = IntVar()
similarityOptionVar = StringVar()
#Main Var
custEntry = StringVar()
summaryLabelVar = StringVar()
summaryLabelVar2 = StringVar()
summaryLabelVar3 = StringVar()
suggestLabelVar = StringVar()
suggestLabelVar2 = StringVar()
orderOk = StringVar()
output = StringVar()
#Edit Var
removeLabelVar = StringVar()
eVar = StringVar()
#productLookup 
prodLvar = StringVar()
prodName = StringVar()
prodCat = StringVar()
prodPrice = StringVar()
prodSize = StringVar()
#Frames
#------
#Add order frame 
newOrderFrame = Frame(cbrGui)
newOrderFrameLabel = Label(newOrderFrame, textvariable = newCustIdVar).pack()
newOrderFrameLabel1 = Label(newOrderFrame, text="Products:").pack()
newOrderFrameLabel2 = Label(newOrderFrame, textvariable = newCustProductsVar).pack()

addOrderProd = Entry(newOrderFrame,textvariable = eVar).pack(side=LEFT)
addOrderBut = Button(newOrderFrame,text = "Remove", command = removeProd).pack(side=LEFT)
addOrderBut2 = Button(newOrderFrame,text = "Add", command = addProd).pack(side=LEFT)
addOrderBut3 = Button(newOrderFrame,text ='Ok',command = writeOrd).pack(side=BOTTOM)
#Configure Frame
configureFrame = Frame(cbrGui)
similarityLabel = Label(configureFrame, text = "Set the minimum similarity (Def = 0.3): ").pack(side=LEFT)
similarityOption = Entry(configureFrame,textvariable = similarityOptionVar).pack(side=LEFT)
setSimButton = Button(configureFrame,text = "Set", command = setSim).pack(side=LEFT)
radioFrame = Frame(cbrGui)

test4=Radiobutton(radioFrame, text="Quantitive", variable=v, value=1).pack(anchor=W)
test5=Radiobutton(radioFrame, text="Qualitative + Quantitive", variable=v, value=0).pack(anchor=W)
#Main Frame
mainFrame = Frame(cbrGui)
mainFrame.pack()
custIdLab = Label(mainFrame,text = 'Enter Customer ID:').pack()
custE = Entry(mainFrame,textvariable = custEntry).pack()
custIdBut = Button(mainFrame,text ='Go',command = main).pack()
output = Text(mainFrame)
summaryLabel = Label(mainFrame, textvariable = summaryLabelVar).pack() #mainframe to show finished
#Summary Frame
summaryFrame = Frame(cbrGui)
summaryLabel2 = Label(summaryFrame, textvariable = summaryLabelVar2).pack()
summaryLabel3 = Label(summaryFrame, textvariable = summaryLabelVar3).pack()
suggestLabel = Label(summaryFrame, textvariable = suggestLabelVar).pack()
suggestLabel2 = Label(summaryFrame, textvariable = suggestLabelVar2).pack()
#Options Frame
ordOptionsFrame = Frame(cbrGui)
ordEditBut = Button(ordOptionsFrame,text ='Edit',command = editOrd).pack(side=LEFT)
ordOkBut = Button(ordOptionsFrame,text ='Ok',command = writeOrd).pack(side=LEFT)
#Edit Frame
editFrame = Frame(cbrGui)
removeLabel = Label(editFrame, textvariable = removeLabelVar).pack()
removeE = Entry(editFrame,textvariable = eVar).pack(side=LEFT)
removeButton = Button(editFrame,text = "Remove", command = removeProd).pack(side=LEFT)
addButton = Button(editFrame,text = "Add", command = addProd).pack(side=LEFT)
#ProductLookup
productLookupFrame = Frame(cbrGui)
productLookupFrame.pack(side=BOTTOM)
productLookupLabel = Label(productLookupFrame, text="Enter product to lookup").pack()
productLookupE = Entry(productLookupFrame,textvariable = prodLvar).pack(side=LEFT)
productLookupButton = Button(productLookupFrame,text = "Lookup", command = lookUpProduct).pack(side=LEFT)
#lookupResults
productLookupResults = Frame(cbrGui)
productLookupResults.pack(side=BOTTOM)
productLookupName = Label(productLookupResults, textvariable = prodName).pack()
productLookupCat = Label(productLookupResults, textvariable = prodCat).pack()
productLookupPrice = Label(productLookupResults, textvariable = prodPrice).pack()
productLookupSize= Label(productLookupResults, textvariable = prodSize).pack()
cbrGui.mainloop()

