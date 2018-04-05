# Set Working Directory to your source file; insert double \
#import os
# General Resourceful Engineers File
#os.chdir("C:\\Users\\ruiyicx\\Documents\\SUTD Subjects\\ESD Term 7\\01.112 Machine Learning\\Project")

# CN File
#os.chdir("C:\\Users\\ruiyicx\\Documents\\SUTD Subjects\\ESD Term 7\\01.112 Machine Learning\\Project\\CN\\CN")

def get_data(data):
	dictionary = {}
	raw_data = open(data, 'r', encoding= "utf8")	# r+ is Special read and write mode, which is used to handle both actions when working with a file
	d = raw_data.read()
	# print (d)
	words = d.split('/n')
	for words2 in words:
		words3 = words2.split('\n')
		words4 = words2.rsplit()
		# The words are split in the list format.
	# print(words3)

	# Create a nested list, with the words in the first nested list, and the tags in the second nested list
	# [[words], [tags]]
	lst = [[] for x in range(2)]
	for w in words4:
		if w == 'O' or w == 'B-neutral' or w == 'B-negative' or w == 'B-positive' or w == 'I-neutral' or w == 'I-negative' or w == 'I-positive':
			lst[1].append(w)
		else:
			lst[0].append(w)

	# Create a list, with the total count of tags

	# Create a list, that counts the occurrence of words by tags

	countu = words4.count('O')
	print(countu)
	# print(lst)
	# for item in 

		
	# print(dictionary)

#EN
dirEN_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/train'
dirEN_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.in'
dirEN_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.out'

get_data(dirEN_train)