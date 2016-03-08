import fetcher
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import sys

queue=[]
count=0 #count for the total number of websites
# note that for 2000 html pages, I finish crawling those urls being
# pointed to after 2000 pages already in the dictionary, so in the end 
# the total number of url might be larger than 2000

dictionary_in={} # the dictionary for in degree
dictionary_out={} # the dictionary for out degree

G=nx.Graph()

queue.append('http://www.caltech.edu')

while len(queue)>0 and count<=2000:
	current=queue.pop(0)
	# screening of the outgoing urls
	if "jstor" in current or "ieeexplore" in current or "onlinelibrary" in current or ".pdf" in current:
		continue
	if not "caltech.edu" in current:
		continue

	print current

	sys.stdout.write('\r')
    # the exact output you're looking for:
	sys.stdout.write("[%-40s] %f%%" % ('='*(count/50), count/20))
	sys.stdout.write('\r')
	sys.stdout.flush()

	if current in dictionary_out.keys():
		continue # already crawled before

	G.add_node(current)

	try: 
		addin=fetcher.fetch_links(current) # the new outgoing urls
	except:
		print "*** Something bad happened (404)***\n"
		continue

	try: 
		for item in addin:
		# screening of the outgoing urls
			if "jstor" in item or "ieeexplore" in item or "onlinelibrary" in item or ".pdf" in item:
				continue
			if not "caltech.edu" in item:
				continue
			if item in dictionary_in.keys():
				dictionary_in[item]+=1
			else:
				dictionary_in[item]=1
			G.add_edge(current, item)
	except: 
		print "*** Something bad happened (NoneType Obj)***\n"
		continue

	count+=1
	dictionary_out[current]=0
	dictionary_out[current]+=len(addin)
	queue.extend(addin)

'''
while len(queue)>0:
	current=queue.pop(0)
	if current in dictionary_out.keys():
		continue
	count+=1
	try:
		addin=fetcher.fetch_links(current)
	except Exception, e:
		print "Something happened\n"
		continue
	
	for item in addin:
		if item in dictionary_in.keys():
			dictionary_in[item]+=1
		else:
			dictionary_in[item]=1
	dictionary_out[current]=len(addin)
'''
# there is too many urls in the queue after 2000 pages being crawled
# so just finish the crawling by matching dictionary_in with dictionary_out
for item in dictionary_out.keys():
	if not dictionary_in[item]:
		dictionary_in[item]=0
# output in-degree and out-degree log
f1=open('./output.txt', 'w+')
idx=0
indeg=[]
outdeg=[]
for item in dictionary_out.keys():
	f1.write(str(idx))
	f1.write(' ')
	f1.write(item)
	f1.write(' ')
	f1.write(str(dictionary_in[item]))
	f1.write(' ')
	f1.write(str(dictionary_out[item]))
	f1.write('\n')
	idx+=1
	indeg.append(dictionary_in[item])
	outdeg.append(dictionary_out[item])

# plot
#--------------------------------------------------
nx.draw_random(G)
plt.title("Websites network diagram")
plt.show()

#--------------------------------------------------
N=np.arange(min(indeg), max(indeg))
plt.hist(indeg, N)
plt.title("Degree Histogram of Indegree")
plt.grid(True)
plt.xlabel("Value of degree")
plt.ylabel("Frequency")
plt.show()

N=np.arange(min(outdeg), max(outdeg))
plt.hist(outdeg, N)
plt.title("Degree Histogram of Outdegree")
plt.grid(True)
plt.xlabel("Value of degree")
plt.ylabel("Frequency")
plt.show()

# ccdf
#----------------------------------------------------
p = 1. * np.arange(len(indeg)) / (len(indeg) - 1)
indeg_sorted=np.sort(indeg)
plt.plot(indeg_sorted, 1-p)
plt.ylabel("P of in indegree")
plt.xlabel("ccdf")
plt.title("complementary cumulative distribution function")
plt.show()

p = 1. * np.arange(len(outdeg)) / (len(outdeg) - 1)
outdeg_sorted=np.sort(outdeg)
plt.plot(outdeg_sorted, 1-p)
plt.ylabel("P of out outdegree")
plt.xlabel("ccdf")
plt.title("complementary cumulative distribution function")
plt.show()

avg_clustering_coeff=nx.average_clustering(G) 
print avg_clustering_coeff
global_clustering_coeff=nx.transitivity(G) 
print global_clustering_coeff

diam=nx.diameter(G)
print diam
lG=nx.average_shortest_path_length(G)
print lG



