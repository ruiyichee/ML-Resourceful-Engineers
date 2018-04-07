# Set Working Directory to your source file; insert double \
# import os
# General Resourceful Engineers File
# os.chdir("C:\\Users\\ruiyicx\\Documents\\SUTD Subjects\\ESD Term 7\\01.112 Machine Learning\\Project")

# CN File
# os.chdir("C:\\Users\\ruiyicx\\Documents\\SUTD Subjects\\ESD Term 7\\01.112 Machine Learning\\Project\\CN\\CN")
ggdict = {}
nesteddict = {"B-positive": 0,"B-negative":0,"B-neutral":0,"I-positive":0,"I-negative":0,"I-neutral":0,"O":0}

def get_data(data):
	global ggdict
	global nesteddict
	dictionary = {}
	raw_data = open(data, 'r', encoding= "utf8")	# r+ is Special read and write mode, which is used to handle both actions when working with a file
	d = raw_data.read()
	#print(d)
	words = d.split('/n')
	#print(ggdict,"\nhi")
	for words2 in words:
		globaldict = {}
		words3 = words2.split('\n') ##words3 is a list of pairs of words and their labels
		for i in range(len(words3)):
			spt = words3[i].split(" ")
			if len(spt) > 3 or len(spt) <2:
				continue
			#print(spt)
			key1 = spt[0]
			label1 = spt[1]
			if key1 not in globaldict:
				globaldict[key1] = nesteddict
				globaldict[key1][label1] += 1
			nesteddict = {"B-positive": 0, "B-negative": 0, "B-neutral": 0, "I-positive": 0, "I-negative": 0,
							  "I-neutral": 0, "O": 0}
		for k in globaldict:
			vdict = globaldict[k]
			if k not in ggdict:
				ggdict[k] = vdict
			else:
				for k1,v in vdict.items():
					ggdict[k][k1] += v

		words4 = words2.rsplit()
	#print(words3)

	# Develop a dictionary, taking the occurrences of the key as the value
	# for w in words3:
	# 	if w not in dictionary:
	# 		dictionary[w] = 1
	# 	else:
	# 		dictionary[w] += 1

	countu = words4.count('O')
	print(countu)
	# print("ggdict:%s" %ggdict)



# EN
dirEN_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/train'
dirEN_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.in'
dirEN_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.out'
get_data(dirEN_train)
# dirEN_train = get_data('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/train')
# dirEN_in = get_data('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.in')
# dirEN_out = get_data('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.out')
# get_data('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/train')
# 
#print(globaldict["@dawngpsalm63"])
#print(nesteddict)

