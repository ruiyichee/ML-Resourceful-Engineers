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
	print(words3)

	# Develop a dictionary, taking the occurrences of the key as the value
	for w in words3:
		if w not in dictionary:
			dictionary[w] = 1
		else:
			dictionary[w] += 1

	countu = words4.count('O')
	print(countu)

		
	# print(dictionary)
#EN
#dirEN_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/train'
#dirEN_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.in'
#dirEN_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.out'

dirEN_train = get_data('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/train')
dirEN_in = get_data('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.in')
dirEN_out = get_data('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.out')


