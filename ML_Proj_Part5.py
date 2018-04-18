import numpy as np
import os

from datetime import datetime
start_time = datetime.now()

# dirEN_train =('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/train')
# dirEN_in =('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.in')
# dirEN_out =('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.out')

def modifytestfile(trainfile, testfile):
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
            '''

            for i in range(len(train_data)):
                if train_data[i][0] == spt [1]: #if the label in the training_data list is the same as the label of the training data
                    if spt[0] in train_data[i][1]:
                        train_data[i][1][spt[0]]+=1
                    else:
                        train_data[i][1][spt[0]] = 1
                else:
                    train_data[i][1][spt[0]]=0
            key1 = spt[0] #'Trump', 'tour', 'bus'
            words_in_train.append(key1)
    '''
    print (train_data)
    [['B-positive', {'digital': 1, 'Sens': 1, 'Mathews': 1, 'Knock': 1, 'Aberfan': 1, 'Jon': 1, ...
     ['B-negative', {"Donny's": 1, 'Sticks': 1, 'Tesco': 2, 'parasites': 1, 'Singapore': 2, ...
    '''
    raw_test = open(testfile, 'r+', encoding="utf8")
    words_in_test = []
    read_lines =raw_test.read()
    lines = read_lines.split('\n')
    for words in lines:
        try:
            words_in_test.append(words)
        except:
            words_in_test.append('')

    modified_test = []
    # modified_test is a list that counts the number of times the words appear in test file, in the same order as the words in trainfile
    for word in words_in_train:
        count = 0
        if word in words_in_test:
            count += words_in_test.count(word)
        modified_test.append(count)

    return words_in_train, train_data, modified_test, words_in_test

def training(words_in_train,train_data,iterations,theta0): #takes training data as input, returns theta vector
    label_list = ["B-positive", "B-negative","B-neutral","I-positive","I-negative","I-neutral","O"]

    '''
    # initializes a vector of zeroes for the different labels, +1 to accomodate theta0
    {'B-positive': array([0, 0, 0, ..., 0, 0, 0]), 'B-negative': array([0, 0, 0, ..., 0, 0, 0]), 'B-neutral': array([0, 0, 0, ..., 0, 0, 0]),
    '''

    for i in range(iterations):
        for label,word_dict in train_data:
            word_count_list = []  # word count of all the words in the trainfile for the particular label
            '''
            # print(word_dict)
            #label would show B-positive, B-negative
            #word_dict shows a dictionary of all the 69k words {"Donny's": 1, 'Sticks': 1, 'Tesco': 2, 'parasites': 1}
            '''
            for i in range(len(words_in_train)): # iterate through 69k times
                word = words_in_train[i]
                if word in word_dict: # if for that particular label, the word is in the word dictionary
                    word_count_list.append(word_dict[word])
                    # appends the count for that partcular word in the corresponding label
            word_count_list.append(theta0)
            # word_count_list is a list of the counts of words [1, 1, 1, 1, 6, 15, 6, 2, 6, 1, 6, 6, 1, 1, 3, 1
            train_array = np.array(word_count_list)
            argmax = 0 #initialize the argmax
            predicted_label = label_list[0]
             #initialise the first label to be "B-positive"

            theta_vector = {c: np.array([0 for i in range(len(word_count_list))]) for c in label_list}

            for i in range(len(label_list)):

                key1 = label_list[i] # key1 = "B-positive"
                thetav = theta_vector[key1] # the specific theta for the label
                learning = np.dot(word_count_list, thetav) # this is the learning phase, theta dot x = y

                if learning >= argmax:
                    argmax = learning
                    predicted_label = label_list[i]

                    if label != predicted_label: # if the label is wrongly predicted, update the theta
                        theta_vector[label] += word_count_list # add vector to the correct weight
                        theta_vector[predicted_label] -= word_count_list # minus the vector from the wrong weight
                        # this allows for a more accurate learning of theta
    print(theta_vector)
    return theta_vector

def predict(count_words_in_test, theta_vector, words_in_test, words_in_train, theta0):
    # initialisation
    count_words_in_test.append(theta0)
    output_file = open("dev.p5.out", "w+", encoding="utf8")
    testwords = []
    tag = []
    counter = 0

    for word in words_in_test: # iterate through every word in the testfile
        counter += 1
        # output_file.write(word + " ")
        word_vector = [0] * len(count_words_in_test)
        argmax = 0
        predicted_label = "B-positive"

        if word in words_in_train:
            testwords.append(word)
            index = words_in_train.index(word)
            word_vector[index] = 1

            for k in theta_vector.keys():
                # iterate with the different label thetas as well. k is the labels "B-positive", "B-negative" etc
                threshold = np.dot(word_vector,theta_vector[k])
                # print(threshold)
                if threshold >= argmax:
                    argmax = threshold
                    predicted_label = k
                    tag.append(predicted_label)
        elif word == "":
            testwords.append("")
            tag.append("")            
        else:
            testwords.append(word)
            tag.append("unknown")

    for i in range(0,counter):
        output_file.write("%s %s\n" % (testwords[i], tag[i]))

    output_file.close()
    return output_file


#RU
os.chdir('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU')
dirRU_train =('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/train')
dirRU_in =('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/dev.in')
dirRU_out =('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/dev.out')
words_in_train_RU, train_data_RU, count_words_in_test_RU, words_in_test_RU = modifytestfile(dirRU_train,dirRU_in)
theta_vector_RU = training(words_in_train_RU, train_data_RU,10,1)
predict(count_words_in_test_RU, theta_vector_RU, words_in_test_RU, words_in_train_RU,1)
print("RU DONE")
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

#ES
os.chdir('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES')
dirES_train =('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/train')
dirES_in =('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/dev.in')
dirES_out =('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/dev.out')
words_in_train_ES, train_data_ES, count_words_in_test_ES, words_in_test_ES = modifytestfile(dirES_train,dirES_in)
theta_vector_ES = training(words_in_train_ES, train_data_ES,10,1)
predict(count_words_in_test_ES, theta_vector_ES, words_in_test_ES, words_in_train_ES,1)
print("ES DONE")
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))