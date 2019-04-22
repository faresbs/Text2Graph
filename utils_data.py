"""
utils data helper scripts for dataset 'debates'
"""
import os
import re
from collections import Counter
import csv
import copy

#Dictionary to save pairings alongside their weights
#This is a global variable
dic = {}

#Tranform to lookup table, elements to int
def lookup(l):

	#Get rid of duplicates if there is
	result = []
	
	for value in l:
		# If value has not been encountered yet,
		# ... add it to both list and set.
		if value not in result:
			result.append(value)
	
	#Save elements with their int value
	table = {}
	i = 0
	for element in result:
		table.update({element: i})
		i += 1

	return table

#retrive common words in text
def common(corpus, k=100):

	with open(corpus, "r", encoding="utf-8") as file:

		data = file.read()
		#print(data)

		# split() returns list of all the words in the string 
		split_it = data.split() 
		  
		# Pass the split_it list to instance of Counter class. 
		counter = Counter(split_it) 
		  
		# most_common() produces k frequently encountered 
		# input values and their respective counts. 
		most_occur = counter.most_common(k) 
		  
		print(most_occur) 

	return most_occur


#Helper function, match two distinct elements in a string
def edge(line, common):

	#Change in global variable
	global dic

	#Avoid modifying original list
	keywords = copy.deepcopy(common)

	found = []
	line = line.split(' ')
	#remove \n at the end
	line[-1] = line[-1].strip()

	#print(len(keywords))
	#print(keywords)
	
	#keywords = set(keywords)
	#print(keywords)
	#print(len(keywords))

	for l in line:

		if (l in keywords):
			found.append(l)
			#remove element for list
			keywords.remove(l)

	#Generate all possible pairings 
	result = []
	for p1 in range(len(found)):
		for p2 in range(p1+1,len(found)):
			result.append([found[p1],found[p2]])


	#Only if element doesnt already exist in dic
	#Check if pairing exist in any order
	#if(all(elem in x for elem in dic)):
	if(len(result)>0):
		#Transform list to tuple
		result = tuple(tuple(x) for x in result)
		for x in result:
			if(x in dic):
				dic[x] += 1
			else:
				dic.update({x: 1})



#Keep lines that has 2 common words
#Put Weights of an edge connecting two named entities
#Number of times entities appear together in our dataset is the weight
def keep(common, table):
	
	with open('final_corpus.csv', 'w') as writeFile:
	
		writer = csv.writer(writeFile, delimiter =' ')
		
		#Loop over the corpuses
		for d in range(len(debates)):
			corpus ='data/corpus/'+str(d)+'.txt'

			with open(corpus, "r") as text:
				for i, line in enumerate(text):
					#if any(s in line for s in common):
					#If it has 2 common words
					edge(line, common)
					#print(len(common))
	
		#print(dic)
		for key, weight in dic.items():
			#Write two index from lookup table and their weight
			writer.writerow([table[key[0]], table[key[1]], weight])
					
	writeFile.close()			

def read_data(PATH):
	debates = os.listdir(PATH)

	d = 0
	count = 0

	for debate in debates:
		files = os.listdir(PATH+'/'+debate)
		
		with open('data/corpus/'+str(d)+'.txt', 'w') as output:

			#Loop over files for every debate
			for file in files:
				current_file = PATH+'/'+debate+'/'+file
				#Avoid encoding problems
				with open(current_file, encoding="ISO-8859-1") as text:
					for i, line in enumerate(text):
						#Get rid of unwanted lines
						if not line.startswith('#'):
							#Split into sentences
							sentences = line.split('.')

							for sentence in sentences:
								#Remove special characters except spaces
								s = re.sub(r"[^a-zA-Z]+", ' ', sentence)

								if(len(s) != 0):
									output.write(s+'\n')
				
		print(debate)
		d += 1
		


if __name__ == '__main__':

	###Create corpus

	#read_data("data/debates")
	
	###Create common words

	debates = os.listdir('data/debates')

	#for i in range(len(debates)):
	#	with open('data/common_words/'+str(i)+'.txt', 'w') as f:
	#		most_occur = common('data/corpus/'+str(i)+'.txt')
	#		for i in most_occur:
	#			f.write(str(i[0])+'\n')


	###Create final corpus

	#Concatenate the common words
	common = []
	for i in range(len(debates)):
		#Read common words
		with open('data/common_words/'+str(i)+'.txt', 'r') as f:
			for line in f.readlines():
				common.append(line.replace('\n', ''))

	## TO DO: save words with their indices !!!
	table = lookup(common)

	keep(common, table)
		