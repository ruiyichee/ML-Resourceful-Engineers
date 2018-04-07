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


# EN
dirEN_train = get_data('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/train')
dirEN_in = get_data('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.in')
dirEN_out = get_data('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.out')
emission_par(dirEN_train)

# dirEN_train = get_data('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/train')
# dirEN_in = get_data('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.in')
# dirEN_out = get_data('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.out')
# emission_par(dirEN_train)
