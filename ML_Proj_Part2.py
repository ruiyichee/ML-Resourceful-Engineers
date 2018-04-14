# General Resourceful Engineers File

# from datetime import datetime
# start_time = datetime.now()
import os

ggdict = {}
nesteddict = {"B-positive": 0, "B-negative": 0, "B-neutral": 0, "I-positive": 0, "I-negative": 0, "I-neutral": 0,
              "O": 0}

def get_data(data):
    raw_data = open(data, 'r',
                    encoding="utf8")  # r+ is Special read and write mode, which is used to handle both actions when working with a file
    d = raw_data.read()
    words = d.split('/n')
    return words

def modified_test(trainfile, testfile):
    raw_train = open(trainfile, 'r+',
                     encoding="utf8")  # r+ is Special read and write mode, which is used to handle both actions when working with a file

    words_in_train = []
    for words2 in raw_train:
        words3 = words2.split('\n')  ##words3 is a list of pairs of words and their labels
        for i in range(len(words3)):
            spt = words3[i].split(" ")
            if len(spt) > 3 or len(spt) < 2:
                continue
            # print(spt)
            key1 = spt[0]
            words_in_train.append(key1)

    # print(words_in_train)
    raw_test = open(testfile, 'r+',
                    encoding="utf8")  # r+ is Special read and write mode, which is used to handle both actions when working with a file
    words_in_test = []
    read_lines = raw_test.read()
    lines = read_lines.split('\n')
    for words in lines:
        try:
            words_in_test.append(words)
        except:
            words_in_test.append('')
    modified_test = words_in_test

    kcount = 0
    for x in range(len(words_in_test)):
        if words_in_test[x] == '':
            modified_test[x] = modified_test[x]
        elif words_in_test[x] not in words_in_train:
            modified_test[x] = '#UNK#'
            kcount += 1

    return modified_test, kcount

def emission_par(words,kcount):
    global ggdict
    global nesteddict

    totalcountBpos = 0
    totalcountBneg = 0
    totalcountBneu = 0
    totalcountIpos = 0
    totalcountIneg = 0
    totalcountIneu = 0
    totalcountO = 0
    tag_count = {}
    for words2 in words:
        globaldict = {}
        words3 = words2.split('\n')  ##words3 is a list of pairs of words and their tags
        for i in range(len(words3)):
            spt = words3[i].split(" ")
            if len(spt) > 3 or len(spt) < 2:
                continue
            # print(spt)
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

        for k in globaldict:  ##k refers to the words in the smaller global dictionary
            vdict = globaldict[k]  ##vdict refers to the existing dictionary of label counts for the particular word k
            if k not in ggdict:  ## if the word k does not exist in the global global dictionary
                ggdict[k] = vdict  ## update the global global dictionary with the existing dictionary of label counts
            else:
                for k1, v in vdict.items():
                    ggdict[k][k1] += v  ##add the label counts to the global global dictionary
        ggdict['#UNK#']= {"B-positive": kcount, "B-negative": kcount, "B-neutral": kcount, "I-positive": kcount, "I-negative": kcount, "I-neutral": kcount, "O": kcount}
        # Calculating the emission parameters
        for word, tagdict in ggdict.items():
            for tag, count in tagdict.items():
                if tag == 'B-positive':
                    ggdict[word][tag] = ggdict[word][tag] / (totalcountBpos +kcount)
                elif tag == 'B-negative':
                    ggdict[word][tag] = ggdict[word][tag] / (totalcountBneg +kcount)
                elif tag == 'B-neutral':
                    ggdict[word][tag] = ggdict[word][tag] / (totalcountBneu +kcount)
                elif tag == 'I-positive':
                    ggdict[word][tag] = ggdict[word][tag] / (totalcountIpos +kcount)
                elif tag == 'I-negative':
                    ggdict[word][tag] = ggdict[word][tag] / (totalcountIneg +kcount)
                elif tag == 'I-neutral':
                    ggdict[word][tag] = ggdict[word][tag] / (totalcountIneu +kcount)
                else:
                    ggdict[word][tag] = ggdict[word][tag] / (totalcountO +kcount)
    # print("ggdict: %s" %ggdict)
    # build dictionary of total tag counts for each tag
    tag_count = {"B-positive": totalcountBpos, "B-negative": totalcountBneg, "B-neutral": totalcountBneu, "I-positive": totalcountIpos, "I-negative": totalcountIneg,
                          "I-neutral": totalcountIneu, "O": totalcountO}
    return ggdict, tag_count

def sentiment_analysis(test_file, emission_params):
  #test_file is dev.in file , output_file is the output of the maximized probabilities of the tags for the words in dev.in, emission_params is the ggdict
    testwords = []
    tag = []
    counter = 0

    for w in test_file:
        counter += 1
        if w in emission_params.keys():
            tagdict = emission_params[w]
            testwords.append(w)
            tag.append(max(tagdict,key=tagdict.get))
        elif w == "#UNK#":
            testwords.append("#UNK#")
            UNKtag = max(emission_params['#UNK#'], key= emission_params['#UNK#'].get)
            tag.append(UNKtag)
        else:
            testwords.append("")
            tag.append("")
    #print(counter)

    f = open("dev.p2.out", "w+", encoding="utf8")
    for i in range(0,counter):
        f.write("%s %s\n" % (testwords[i],tag[i]))
    f.close()
    print('DONE')

    # for key,value in output.items():
    #     if value == "#UNK#":
    #         f.write("%s %s\n" % ("#UNK#", UNKtag))
    #     else:
    #         f.write("%s %s\n" % (key,value))
    # f.close()
    # print('DONE')

# EN
# RUIYI
os.chdir('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN')
dirEN_train = ('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/train')
dirEN_in = ('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.in')
dirEN_out = ('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/EN/EN/dev.out')
dirEN_test = ('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/modified_file.txt')
## EN
modified_test_EN, kcount_EN = modified_test(dirEN_train, dirEN_in)
emission_param_EN, tag_count_EN = emission_par(get_data(dirEN_train),kcount_EN)
sentiment_analysis(modified_test_EN, emission_param_EN)
print("EN DONE")

# CN
os.chdir('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/CN/CN')
dirCN_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/CN/CN/train'
dirCN_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/CN/CN/dev.in'
dirCN_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/CN/CN/dev.out'
dirCN_test = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/CN/CN/modified_file.txt'
## CN
modified_test_CN, kcount_CN = modified_test(dirCN_train, dirCN_in)
emission_param_CN, tag_count_CN = emission_par(get_data(dirCN_train),kcount_CN)
sentiment_analysis(modified_test_CN, emission_param_CN)
print("CN DONE")

# ES
os.chdir('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES')
dirES_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/train'
dirES_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/dev.in'
dirES_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/dev.out'
dirES_test = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/modified_file.txt'
## ES
modified_test_ES, kcount_ES = modified_test(dirES_train, dirES_in)
emission_param_ES, tag_count_ES = emission_par(get_data(dirES_train),kcount_ES)
sentiment_analysis(modified_test_ES, emission_param_ES)
print("ES DONE")

# RU
os.chdir('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU')
dirRU_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/train'
dirRU_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/dev.in'
dirRU_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/dev.out'
dirRU_test = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/modified_file.txt'
## RU
modified_test_RU, kcount_RU = modified_test(dirRU_train, dirRU_in)
emission_param_RU, tag_count_RU = emission_par(get_data(dirRU_train),kcount_RU)
sentiment_analysis(modified_test_RU, emission_param_RU)
print("RU DONE")

# REGINA
# dirEN_train = ('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/train')
# dirEN_in = ('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.in')
# dirEN_out = ('C:/Users/Regina/Documents/SUTD/ESD Term 5/Machine Learning/Project/EN/EN/dev.out')

# end_time = datetime.now()
# print('Duration: {}'.format(end_time - start_time))