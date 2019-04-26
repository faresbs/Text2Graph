#Create knowledge graph from embeddings and cluster using K-means
import numpy as np
from sklearn.cluster import KMeans
import csv

def read(filename):
	#(69, 129)
	file = np.genfromtxt(filename, delimiter=' ', skip_header=1)
	#print(file.shape)
	y = file[:, 0]
	y = y.astype(int)
	x = file[:, 1:]
	#print(x)
	#print(y)
	#print(x.shape) #(69,128)
	#print(y.shape) #(69)
	return x, y

def kmeans(x, y, n_c = 6):
	#Use representation context vector (128) to cluster the nodes
	kmeans = KMeans(n_clusters=n_c, random_state=0).fit(x)
	clusters = kmeans.predict(x)

	return clusters

#prepare data for gephi for graph viz
def prepare(y, clusters, clustered=True, sort=True):

	#1 Step: Prepare a node sheet
	if(clustered):
		#Stack id of node w/ is cluster
		a = np.zeros([y.shape[0], 2], dtype=int)

		if(sort):
			#Sort clusters according to y id words
			clusters = [x for _,x in sorted(zip(y,clusters))]

		y.sort()

		a[:, 0] = y
		a[:, 1] = clusters
		#print(a.shape) #(69, 2)

		#Save words w/ their clusters
		with open('nodes.csv', 'w') as out:
		    writer = csv.writer(out, delimiter =' ')
		    writer.writerow(["Id", "Cluster"])
		    #Loop over the nodes
		    for i in range(a.shape[0]):
		    	row = a[i, :]
		        writer.writerows([row])


	#2 step: Prepare edge sheet
	filename = 'final_corpus.csv'

	with open('edges.csv', 'wb') as out:
	    writer = csv.writer(out, delimiter =' ')
	    writer.writerow(["Source", "Target", "Weight"])

	    with open(filename, 'r') as incsv:
	        reader = csv.reader(incsv)
	        for row in reader:
	        	writer.writerows([row[0].split()])




if __name__ == '__main__':
	#Read the file of embeddings
	filename = 'emb'
	x, y = read(filename)
	clusters = kmeans(x, y)
	prepare(y, clusters, True, True)