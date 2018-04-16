# def get_data(data):
# 	raw_data = open(data, 'r', encoding= "utf8")	# r+ is Special read and write mode, which is used to handle both actions when working with a file
# 	read = raw_data.read()
# 	print (read)

import numpy as np

dirEN_train =('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/train')
dirEN_in =('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.in')
dirEN_out =('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.out')

def modified_test(trainfile, testfile):
    raw_train = open(trainfile, 'r+',
                     encoding="utf8")  # r+ is Special read and write mode, which is used to handle both actions when working with a file

    words_in_train = [] #this is a list of all the words X_i from the training data
    train_data = [["B-positive",{}], ["B-negative",{}], ["B-neutral",{}], ["I-positive",{}], ["I-negative",{}], ["I-neutral",{}], ["O",{}]]
    for words2 in raw_train:
        words3 = words2.split('\n')  ##words3 is a list of pairs of words and their labels
        '''
        words3 appears like this
        ['for O', '']
        ['8 O', '']
        ['years O', '']
        ['but O', '']
        ['then O', '']
        ['stumbled O', '']
        '''
        for i in range(len(words3)):
            spt = words3[i].split(" ")

            if len(spt) > 3 or len(spt) < 2:
                continue
            '''
            print(spt)
            ['Trump', 'B-neutral']
            ['tour', 'O']
            ['bus', 'O']
            ['video', 'O']
            ['out', 'O']
            ['in', 'O']
            ['8', 'O']
            '''
            for i in range(len(train_data)):
                if train_data[i][0] == spt [1]: #if the label in the training_data list is the same as the label of the training data
                    if spt[0] in train_data[i][1]:
                        train_data[i][1][spt[0]]+=1
                    else:
                        train_data[i][1][spt[0]] = 1
            key1 = spt[0] #'Trump', 'tour', 'bus'
            words_in_train.append(key1)

    '''
    print (train_data)
    [['B-positive', {'digital': 1, 'Sens': 1, 'Mathews': 1, 'Knock': 1, 'Aberfan': 1, 'Jon': 1, ...
     ['B-negative', {"Donny's": 1, 'Sticks': 1, 'Tesco': 2, 'parasites': 1, 'Singapore': 2, ...
    '''
    return words_in_train, train_data

words_in_train, train_data = modified_test(dirEN_train,dirEN_in)

def multiclassPerceptron(words_in_train,train_data,iterations,theta0): #takes training data as input, returns theta vector
    label_list = ["B-positive", "B-negative","B-neutral","I-positive","I-negative","I-neutral","O"]
    theta_vector = {c: np.array([0 for i in range(len(words_in_train) + 1)]) for c in label_list}
    '''
    # print(theta_vector)
    # initializes a vector of zeroes for the different labels, +1 to accomodate theta0
    {'B-positive': array([0, 0, 0, ..., 0, 0, 0]), 'B-negative': array([0, 0, 0, ..., 0, 0, 0]), 'B-neutral': array([0, 0, 0, ..., 0, 0, 0]), 
    '''

    for i in range(iterations):
        for label,word_dict in train_data: #label is B+, B-, B-neutral, worddict is {'digital': 1, 'Sens': 1, 'Mathews': 1, 'Knock': 1, 'Aberfan': 1,

            # for k in range(len(label_list)):
            #     label_list = train_data[k]
            words_in_train.append(theta0)

            word_vector = np.array(words_in_train)

            argmax = 0 #initialize the argmax
            predicted_label = label_list[0] #initialise the first label to be "B-positive"

            for i in range(len(label_list)):
                ###THERE IS SOMETHING WRONG HERE##
                learning = np.dot(word_vector, theta_vector[i]) #this is the learning phase, theta dot x = y
                if learning >= argmax:
                    argmax = learning
                    predicted_label = label_list[i]

            if label != predicted_label: #if the label is wrongly predicted, update the theta
                theta_vector[label] += word_vector #add vector to the correct weight
                theta_vector[predicted_label] -= word_vector #minus the vector from the wrong weight
                # this allows for a more accurate learning of theta

    return theta_vector

multiclassPerceptron(words_in_train, train_data,10,1)
# class MultiClassPerceptron():
#     def __init__(self, classes, feature_list, feature_data, test_data, iterations=ITERATIONS):
#         self.classes = classes
#         self.feature_list = feature_list
#         self.feature_data = feature_data
#         # self.ratio = train_test_ratio
#         self.iterations = iterations
#
#         # Split feature data into train set, and test set
#         self.train_set = self.feature_data
#         self.test_set = self.test_data
#
#         # Initialize empty weight vectors, with extra BIAS term.
#         self.weight_vectors = {c: np.array([0 for i in range(len(feature_list) + 1)]) for c in self.classes}
#
#     def train(self):
#         for i in range(self.iterations):
#             for category, feature_dict in self.train_set:
#                 # Format feature values as a vector, with extra BIAS term.
#                 feature_list = [feature_dict[k] for k in self.feature_list]
#                 feature_list.append(BIAS)
#                 feature_vector = np.array(feature_list)
#
#                 # Initialize arg_max value, predicted class.
#                 arg_max, predicted_class = 0, self.classes[0]
#
#                 # Multi-Class Decision Rule:
#                 for c in self.classes:
#                     current_activation = np.dot(feature_vector, self.weight_vectors[c])
#                     if current_activation >= arg_max:
#                         arg_max, predicted_class = current_activation, c
#
#                 # Update Rule:
#                 if not (category == predicted_class):
#                     self.weight_vectors[category] += feature_vector
#                     self.weight_vectors[predicted_class] -= feature_vector
#
#     def predict(self, feature_dict):
#         """
#         Categorize a brand-new, unseen data point based on the existing collected data.
#         :param  feature_dictionary  Dictionary of the same form as the training feature data.
#         :return                     Return the predicted category for the data point.
#         """
#         feature_list = [feature_dict[k] for k in self.feature_list]
#         feature_list.append(BIAS)
#         feature_vector = np.array(feature_list)
#
#         # Initialize arg_max value, predicted class.
#         arg_max, predicted_class = 0, self.classes[0]
#
#         # Multi-Class Decision Rule:
#         for c in self.classes:
#             current_activation = np.dot(feature_vector, self.weight_vectors[c])
#             if current_activation >= arg_max:
#                 arg_max, predicted_class = current_activation, c
#
#         return predicted_class
#
#
#
