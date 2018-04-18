# ML Resourceful Engineers
# Chee Rui Yi (1001738), Maylizabeth (1001818), Regina Lim (1001789)

# Part 4 on kbest viterbi algorithm

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

def viterbi_kbest(test_file, transition_par, emission_par, tags, topk, kth):
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
        
    output_file = open("dev.p4.out", "w+", encoding="utf8")
    for s in sentences:
        nodes = calculate_node_scores(s,transition_par,emission_par, tags, topk)
        labelled_sentence = backtracking(s,nodes, kth)

        for word in labelled_sentence:
            output_file.write(word + '\n')
        output_file.write('\n')
    output_file.close()

def calculate_node_scores(s, transition_par, emission_par, tags, topk):
    nodes = {}
    # base case
    nodes[0] = {'START':[[1,'Nil',0]]}
    # recursive
    for k in range (1, len(s)+1): # for each word
        X = s[k-1] # previous node
        for V in tags.keys():# for each node
            prev_nodes_dict = nodes[k-1] # access prev nodes
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

            scores =[]
            
            # transition parameters
            for U in prev_nodes_dict.keys(): # taking the previous node U saved
                prev_states = transition_par[V]
                # if U in prev_states (transition para dictionary): then there is an edge
                if U in prev_states.keys():
                    a = prev_states[U]
                else:
                    # consider the case where U is not in the prev_states; probability = 0
                    a = 0

                index = 0
                # Calculate prev node score
                for prev_k_nodes in prev_nodes_dict[U]:
                    prev_score = prev_k_nodes[0]
                    score = prev_score*a*b
                    scores.append([score, U, index])
                    index += 1

            # take top k scores
            scores.sort(key=lambda x:x[0], reverse=True)
            topk_scores = scores[:topk]
            if k in nodes.keys():
                nodes[k][V] = topk_scores # update the highest_score, parent cos iteration
            else:
                new_dict = {V:topk_scores}
                nodes[k] = new_dict
    # end case
    prev_nodes_dict = nodes[len(s)] # last layer
    scores = []
    # take the U node in order to do transition parameters
    # transition parameters
    for U in prev_nodes_dict.keys():
        prev_states = transition_par['STOP'] # get the probabilities of tags dictionary
        if U in prev_states.keys():
            a = prev_states[U]
        else:
            a = 0
        index = 0
        # prev node score
        for prev_k_nodes in prev_nodes_dict[U]:
            score = prev_k_nodes[0] *a
            scores.append([score, U, index])
            index += 1
    scores.sort(key=lambda x: x[0], reverse=True)
    topk_scores = scores[:topk]
    indiv_node = {'STOP': topk_scores}
    nodes[len(s)+1] = indiv_node

    return nodes

def backtracking(s, nodes,kth):
    prev_state = 'STOP'
    prev_index = 0
    for i in range(len(s)+1, 1, -1): # Start at the end, and iterate backwards one node at a time
        if i == len(s) +1:
            prev_node = nodes[i][prev_state][kth-1]
        else:
            prev_node = nodes[i][prev_state][prev_index]
        prev_state = prev_node[1]
        prev_index = prev_node[2]
        s[i-2] += " " + prev_state # save the prev node
    return s

# ES
os.chdir('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES')
dirES_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/train'
dirES_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/dev.in'
dirES_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/ES/ES/dev.out'
## ES
modified_test_ES, kcount_ES = modified_test(dirES_train, dirES_in)
emission_param_ES, tag_count_ES = emission_par(get_data(dirES_train),kcount_ES)
# sentiment_analysis(modified_test_ES, emission_param_ES)
transition_params_ES = transition_params(dirES_train)
viterbi_kbest(dirES_in, transition_params_ES, emission_param_ES, tag_count_ES, 7,5)
print("ES DONE")

# RU
os.chdir('C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU')
dirRU_train = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/train'
dirRU_in = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/dev.in'
dirRU_out = 'C:/Users/ruiyicx/Documents/SUTD Subjects/ESD Term 7/01.112 Machine Learning/Project/RU/RU/dev.out'
## RU
modified_test_RU, kcount_RU = modified_test(dirRU_train, dirRU_in)
emission_param_RU, tag_count_RU = emission_par(get_data(dirRU_train),kcount_RU)
# sentiment_analysis(modified_test_RU, emission_param_RU)
transition_params_RU = transition_params(dirRU_train)
viterbi_kbest(dirRU_in, transition_params_RU, emission_param_RU, tag_count_RU, 7,5)
print("RU DONE")