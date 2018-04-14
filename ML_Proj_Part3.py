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
        words3 = words2.split('\n')  ##words3 is a list of pairs of words and their tags
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

def transition_params(train_file):
    transition_count ={}
    state_count = {}
    u_state = 'START'
    v_state = 'STOP'

    state_count[u_state] = 0
    state_count[v_state] = 0
    transition_count[v_state] = {}

    with open(train_file, encoding='utf=8') as file:
        for line in file:
            word_pair= line.split()
            if len(word_pair) !=0 and len(word_pair) <3:
                value = word_pair[1]
                #print (value)

                #add value into transition count
                if value in transition_count.keys():
                    value_list=transition_count[value]
                    
                    #count occurence of values
                    if u_state in value_list.keys():
                        value_list[u_state] += 1
                    else:
                        value_list[u_state] = 1

                #for new keys(words)
                else:
                    new_value = {}
                    new_value[u_state] = 1
                    transition_count[value] = new_value

                #add start and stop state counts
                if u_state == 'START':
                    state_count[u_state] += 1
                    state_count[v_state] += 1

                #add to state counts
                if value in state_count.keys():
                    state_count[value] += 1
                else:
                    state_count[value] = 1

                u_state = value

            else:
                value_list=transition_count[v_state]
                if u_state in value_list.keys():
                    value_list[u_state] +=1
                else:
                    value_list[u_state] =1
                u_state = 'START'

    for V in transition_count.keys():
        for U in transition_count[V].keys():
            transition_count[V][U] /= state_count[U]
    return transition_count

def viterbi_algo(test_file, transition_par, emission_par, tags):
    sentences = []
    input_file = open(test_file, encoding = 'utf-8')
    sentence = []
    # Make use of empty line between sentences to get whole sentence
    for line in input_file:
        if len(line.split()) != 0:
            sentence.append(line.split()[0])
        else:
            sentences.append(sentence)
            sentence = []
    # print(sentences)
        
    output_file = open("dev.p3.out", "w+", encoding="utf8")
    for s in sentences:
        nodes = calculate_node_scores(s,transition_par,emission_par, tags)
        labelled_sentence = backtracking(s,nodes)

        for word in labelled_sentence:
            output_file.write(word + '\n')
        output_file.write('\n')
    output_file.close()

def calculate_node_scores(s, transition_par, emission_par, tags):
    nodes = {}
    # base case
    nodes[0] = {'START':[1,'Nil']}
    # recursive
    for k in range (1, len(s)+1): # for each word
        X = s[k-1] # previous node
        for V in tags.keys():# for each node
            prev_nodes_dict = nodes[k-1] # access prev nodes
            highest_score = 0 # initiatise
            parent = 'Nil' # initiatise
            # emission parameters
            if X in emission_par.keys():
                # save the emission parameter dictionary for that word as emission_labels
                emission_labels = emission_par[X]
                # if V, the label node, is in emission_labels
                # in case the there is no node V (label) in the emission_label
                if V in emission_labels:
                    b = emission_labels[V]
                else:
                    b = 0
            else:
                # take #UNK# into account as they are missing words
                b = emission_par['#UNK#'][V]
            
            # transition parameters
            for U in prev_nodes_dict.keys(): # taking the previous node U saved
                prev_states = transition_par[V]
                # if U in prev_states (transition para dictionary): then there is an edge
                if U in prev_states.keys():
                    a = prev_states[U]
                else:
                    # consider the case where U is not in the prev_states; probability = 0
                    a = 0
                
                # Calculate prev node score
                prev_score = prev_nodes_dict[U][0]
                score = prev_score*a*b
                # Adjust the highest score accordingly
                if score >= highest_score:
                    highest_score = score
                    parent = U # previous node
            if k in nodes.keys():
                nodes[k][V] = [highest_score, parent] # update the highest_score, parent cos iteration
            else:
                new_dict = {V:[highest_score,parent]}
                nodes[k] = new_dict
    # end case
    prev_nodes_dict = nodes[len(s)] # last layer
    highest_score = 0 # initialise end node
    parent = 'None' # initialise end node
    # take the U node in order to do transition parameters
    # transition parameters
    for U in prev_nodes_dict.keys():
        prev_states = transition_par['STOP'] # get the probabilities of tags dictionary
        if U in prev_states.keys():
            a = prev_states[U]
        else:
            a = 0
        # prev node score
        prev_score = prev_nodes_dict[U][0]
        score = prev_score*a # there is no output word
        if score >= highest_score:
            highest_score = score
            parent = U # previous node
    indiv_node = {'STOP': [highest_score, parent]}
    nodes[len(s)+1] = indiv_node

    return nodes

def backtracking(s, nodes):
    prev_state = 'STOP'
    for i in range(len(s)+1, 1, -1): # Start at the end, and iterate backwards one node at a time
        prev_node = nodes[i][prev_state]
        prev_state = prev_node[1]
        s[i-2] += " " + prev_state # save the prev node
    return s


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
# sentiment_analysis(modified_test_EN, emission_param_EN)
transition_params_EN = transition_params(dirEN_train)
# print(transition_params_EN)
viterbi_algo(dirEN_in, transition_params_EN, emission_param_EN, tag_count_EN)
print("EN DONE")

# # CN
# os.chdir('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/CN/CN')
# dirCN_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/CN/CN/train'
# dirCN_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/CN/CN/dev.in'
# dirCN_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/CN/CN/dev.out'
# dirCN_test = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/CN/CN/modified_file.txt'
# ## CN
# modified_test_CN, kcount_CN = modified_test(dirCN_train, dirCN_in)
# emission_param_CN = emission_par(get_data(dirCN_train),kcount_CN)
# # sentiment_analysis(modified_test_CN, emission_param_CN)
# print("CN DONE")

# # ES
# os.chdir('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES')
# dirES_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/train'
# dirES_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/dev.in'
# dirES_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/dev.out'
# dirES_test = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/modified_file.txt'
# ## ES
# modified_test_ES, kcount_ES = modified_test(dirES_train, dirES_in)
# emission_param_ES = emission_par(get_data(dirES_train),kcount_ES)
# # sentiment_analysis(modified_test_ES, emission_param_ES)
# print("ES DONE")

# # RU
# os.chdir('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU')
# dirRU_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/train'
# dirRU_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/dev.in'
# dirRU_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/dev.out'
# dirRU_test = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/modified_file.txt'
# ## RU
# modified_test_RU, kcount_RU = modified_test(dirRU_train, dirRU_in)
# emission_param_RU = emission_par(get_data(dirRU_train),kcount_RU)
# # sentiment_analysis(modified_test_RU, emission_param_RU)
# print("RU DONE")