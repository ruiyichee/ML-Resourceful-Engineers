# Set Working Directory to your source file; insert double \
#import os
# General Resourceful Engineers File
#os.chdir("C:\\Users\\ruiyicx\\Documents\\SUTD Subjects\\ESD Term 7\\01.112 Machine Learning\\Project")

# CN File
#os.chdir("C:\\Users\\ruiyicx\\Documents\\SUTD Subjects\\ESD Term 7\\01.112 Machine Learning\\Project\\CN\\CN")

def get_data(data):
	raw_data = open(data, 'r', encoding= "utf8")	# r+ is Special read and write mode, which is used to handle both actions when working with a file
	read = raw_data.read()
	print (read)
#EN
dirEN_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/train'
dirEN_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.in'
dirEN_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.out'

get_data(dirEN_out)