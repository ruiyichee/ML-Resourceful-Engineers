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

directory1 = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/train'

get_data(directory1)