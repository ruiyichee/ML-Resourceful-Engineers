# Set Working Directory to your source file; insert double \
#import os
# General Resourceful Engineers File
#os.chdir("C:\\Users\\ruiyicx\\Documents\\SUTD Subjects\\ESD Term 7\\01.112 Machine Learning\\Project")

# CN File
#os.chdir("C:\\Users\\ruiyicx\\Documents\\SUTD Subjects\\ESD Term 7\\01.112 Machine Learning\\Project\\CN\\CN")

def get_data(data):
	raw_data = open(data, 'r+', encoding= "utf8")	# r+ is Special read and write mode, which is used to handle both actions when working with a file
	d = raw_data.read()
	pairs = d.split('/n')
	for words in pairs:
		words2 = words.split('\n')
		words3 = words.rsplit()
		# The words are split in the list format.
	print(words3)

	# Create a nested list, with the words in the first nested list, and the tags in the second nested list
	# [[words], [tags]]
	# lst = [[] for x in range(2)]

	# Create a dictionary for emission count and tag count
	emission_count = {} 
	tag_count = {}
	for w in words3:
		if w == 'O' or w == 'B-neutral' or w == 'B-negative' or w == 'B-positive' or w == 'I-neutral' or w == 'I-negative' or w == 'I-positive':
			if w not in tag_count:
				tag_count[w] = 1
			else:
				tag_count[w] += 1
		else:
			if w not in emission_count:
				emission_count[w] = 1
			else:
				emission_count[w] += 1

	countu = words3.count('O')
	print(countu)
	# print(lst)
	# for item in 
	
	print(emission_count)
	print(tag_count)

#EN
dirEN_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/train'
dirEN_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.in'
dirEN_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.out'

get_data(dirEN_train)