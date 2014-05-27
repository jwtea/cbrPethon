from numpy import random,argsort,sqrt
from pylab import plot,show

def knn_search(x, D, K):
	""" find K nearest neighbours of data among D """
	ndata = D.shape[1]
	K = K if K < ndata else ndata
	# euclidean distances from the other points
	sqd = sqrt(((D - x[:,:ndata])**2).sum(axis=0))
	idx = argsort(sqd) # sorting
	# return the indexes of K nearest neighbours
	return idx[:K]

 # knn_search test
data = random.rand(2,200) # random dataset
print data
x = random.rand(2,1) # query point

# performing the search
neig_idx = knn_search(x,data,10)

# plotting the data and the input point
plot(data[0,:],data[1,:],'ob',x[0,0],x[1,0],'or')
# highlighting the neighbours
plot(data[0,neig_idx],data[1,neig_idx],'o',
	markerfacecolor='None',markersize=15,markeredgewidth=1)
show()