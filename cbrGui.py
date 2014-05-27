import fileOps,math
from Tkinter import *
from simMetrics import *
from collections import defaultdict
products = fileOps.openCsv("products.csv")
orders = fileOps.openCsvDebug("cases.csv")
orderDebug = fileOps.openCsvDebug("casesDebug.csv")
newOrderDict = {}
customerProducts = []
orderSimilarity = {}
similarityThreshold = 0.3
#similarityThreshold = raw_input('Enter threshold:')


#Iterate over the CSV. 
def main():
	forgetFrames()
	global newOrderDict
	newOrderDict = {}
	customerProducts = []
	orderSimilarity = {}
	 
	custID = custEntry.get()
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
	suggestLabelVar.set("Suggesting new order of:"+str(newOrderDict['n1']))
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
	
	fileOps.writeRecord(newOrderDict)
	summaryLabelVar.set("New Order Saved")
	forgetFrames()
def addProd():
	global newOrderDict
	present = False
	updatedOrder = {}
	add = eVar.get()
	for key, values in newOrderDict.items():
		updatedOrder.setdefault(key, [])
	        for value in values:
	            updatedOrder[key].append(value)
	            if value == add:
	            	present = True
	        if present != True:
	        	updatedOrder[key].append(add)
	newOrderDict = updatedOrder
	suggestLabelVar.set("Suggesting new order of:"+str(newOrderDict['n1']))
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
	suggestLabelVar.set("Suggesting new order of:"+str(newOrderDict['n1']))
	print "-----"
def editOrd():
	removeLabelVar.set("Enter products to edit")
	editFrame.pack()

def setSim():
	similarityThreshold = similarityOptionVar.get()
	print "sim changed "+ str(similarityThreshold)
#states
def showOptions():
	configureFrame.pack()
	mainFrame.pack_forget()
	summaryFrame.pack_forget()
	ordOptionsFrame.pack_forget()
	editFrame.pack_forget()

def showMain():
	configureFrame.pack_forget()
	mainFrame.pack()
	summaryLabelVar.set("")
	summaryFrame.pack_forget()
	ordOptionsFrame.pack_forget()
	editFrame.pack_forget()

#Setup Gui
cbrGui = Tk()
cbrGui.title("Python CBR")
cbrGui.geometry("500x500")
#Setup Menu
menubar = Menu(cbrGui)
cbrGui.config(menu=menubar)
optionsMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Options", menu = optionsMenu)
optionsMenu.add_command(label = "Suggest new order",command=showMain)
optionsMenu.add_command(label = "View orders",command=forgetFrames)
optionsMenu.add_separator()
optionsMenu.add_command(label = "Configure",command=showOptions)
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
#Frames
#------
#Configure Frame
configureFrame = Frame(cbrGui)
similarityLabel = Label(configureFrame, text = "Set the minimum similarity (Def = 0.3): ").pack(side=LEFT)
similarityOption = Entry(configureFrame,textvariable = similarityOptionVar).pack(side=LEFT)
setSimButton = Button(configureFrame,text = "Set", command = setSim).pack(side=LEFT)
test4=Radiobutton(configureFrame, text="One", variable=v, value=1).pack(anchor=W)
test5=Radiobutton(configureFrame, text="Two", variable=v1, value=1).pack(anchor=W)
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
cbrGui.mainloop()

