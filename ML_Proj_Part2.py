# General Resourceful Engineers File

ggdict = {}
nesteddict = {"B-positive": 0,"B-negative":0,"B-neutral":0,"I-positive":0,"I-negative":0,"I-neutral":0,"O":0}

def get_data(data):
	raw_data = open(data, 'r', encoding= "utf8")	# r+ is Special read and write mode, which is used to handle both actions when working with a file
	d = raw_data.read()
	words = d.split('/n')
	return words

def emission_par(words):
	global ggdict
	global nesteddict

	totalcountBpos = 0
	totalcountBneg = 0
	totalcountBneu = 0
	totalcountIpos = 0
	totalcountIneg = 0
	totalcountIneu = 0
	totalcountO = 0
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

			if label1 == 'B-positive':
				totalcountBpos += 1
			elif label1 == 'B-negative':
				totalcountBneg += 1
			elif label1 == 'B-neutral':
				totalcountBneu += 1
			elif label1 == 'I-positive':
				totalcountIpos += 1
			elif label1 == 'I-negative':
				totalcountIneg += 1
			elif label1 == 'I-neutral':
				totalcountIneu += 1
			else:
				totalcountO += 1

		for k in globaldict: ##k refers to the words in the smaller global dictionary
			vdict = globaldict[k] ##vdict refers to the existing dictionary of label counts for the particular word k
			if k not in ggdict: ## if the word k does not exist in the global global dictionary
				ggdict[k] = vdict ## update the global global dictionary with the existing dictionary of label counts
			else:
				for k1,v in vdict.items():
					ggdict[k][k1] += v ##add the label counts to the global global dictionary

		# Calculating the emission parameters
		for word,tagdict in ggdict.items():
			for tag,count in tagdict.items():
				if tag == 'B-positive':
					ggdict[word][tag] = ggdict[word][tag]/totalcountBpos
				elif tag == 'B-negative':
					ggdict[word][tag] = ggdict[word][tag]/totalcountBneg
				elif tag == 'B-neutral':
					ggdict[word][tag] = ggdict[word][tag]/totalcountBneu
				elif tag == 'I-positive':
					ggdict[word][tag] = ggdict[word][tag]/totalcountIpos
				elif tag == 'I-negative':
					ggdict[word][tag] = ggdict[word][tag]/totalcountIneg
				elif tag == 'I-neutral':
					ggdict[word][tag] = ggdict[word][tag]/totalcountIneu
				else:
					ggdict[word][tag] = ggdict[word][tag]/totalcountO
		print(ggdict)

	# print("ggdict:%s" %ggdict)

	# print(totalcountO)
	# print(totalcountBpos)
	# print(totalcountBneg)
	# print(totalcountBneu)
	# print(totalcountIpos)
	# print(totalcountIneg)
	# print(totalcountIneu)

def modified_test(trainfile,testfile):
	raw_train = open(trainfile, 'r+', encoding= "utf8")	# r+ is Special read and write mode, which is used to handle both actions when working with a file
	# d_train = raw_train.read()
	# words = d_train.split('/n')

	words_in_train = []
	for words2 in raw_train:
		words3 = words2.split('\n') ##words3 is a list of pairs of words and their labels
		for i in range(len(words3)):
			spt = words3[i].split(" ")
			if len(spt) > 3 or len(spt) <2:
				continue
			# print(spt)
			key1 = spt[0]				
			words_in_train.append(key1)
	
	# print(words_in_train)
	raw_test = open(testfile, 'r+', encoding= "utf8")	# r+ is Special read and write mode, which is used to handle both actions when working with a file
	words_in_test = []
	for words2 in raw_test:
		words3 = words2.rsplit()
		# print(words3)
		for i in range(len(words3)):
			key = words3[i]
			words_in_test.append(key)
	modified_test = words_in_test

	kcount = 0
	for x in range(len(words_in_test)):
		if words_in_test[x] not in words_in_train:
			modified_test[x] = '#UNK#'
			kcount += 1
	# print(modified_test)
	# print(kcount)

	f= open("modified_file.txt","w+", encoding= "utf8")
	for item in range(len(modified_test)):
		word = modified_test[item]
		f.write("%s\n" %word)
	f.close()

	return modified_test, kcount


# EN
#RUIYI
# dirEN_train = ('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/train')
# dirEN_in = ('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.in')
# dirEN_out = ('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.out')

#REGINA
dirEN_train=('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/train')
dirEN_in =('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.in')
dirEN_out = ('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.out')

# emission_par(get_data(dirEN_train))
modified_test(dirEN_train, dirEN_in)

