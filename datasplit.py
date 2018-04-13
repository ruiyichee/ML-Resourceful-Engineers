#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 02:36:21 2018

@author: maylizabeth
"""
import numpy as np

train_file=('/Users/maylizabeth/Desktop/ml/EN/dev.out')

#initialise state
state=("B-positive", "B-negative", "B-neutral", "I-positive", "I-negative", "I-neutral","O")
#initialise observations
obs_final=tuple(obs)
#print(obs_final)
obs=[]
with open(train_file, encoding='utf=8') as file:
    #with open(EN_train, encoding='utf=8') as file:
    for line in file:
        word_pair= line.split()
        if len(word_pair) !=0 and len(word_pair) <3:
            value = word_pair[0]
            obs.append(value)
#initialise start_p
start_p= {"B-positive":1/7, "B-negative":1/7, "B-neutral":1/7, "I-positive":1/7, "I-negative":1/7, "I-neutral":1/7,"O":1/7} 
         
EN_train = ('/Users/maylizabeth/Desktop/ml/EN/train')

def transition_params(train_file):
    transition_count ={}
    state_count = {}
    u_state = 'START'
    v_state = 'STOP'

    state_count[u_state] = 0
    state_count[v_state] = 0
    transition_count[v_state] = {}

    with open(train_file, encoding='utf=8') as file:
    #with open(EN_train, encoding='utf=8') as file:
        for line in file:
            word_pair= line.split()
            if len(word_pair) !=0 and len(word_pair) <3:
                value = word_pair[1]
                #print (value)

                #add u_value into transition count
                if value in transition_count.keys():
                    value_list=transition_count[value]
                    
                    #count occurence of values
                    if u_state in value_list.keys():
                        value_list[u_state] += 1
                    else:
                        value_list[u_state] = 1
                     
                #for every other keys
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
                #add v_value to transition count
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

#initialise transition params
transition_params= transition_params(EN_train)
#print (transition_params_EN)

import os
os.chdir('/Users/maylizabeth/Desktop/ml/EN')

ggdict = {}
nesteddict = {"B-positive": 0, "B-negative": 0, "B-neutral": 0, "I-positive": 0, "I-negative": 0, "I-neutral": 0,
              "O": 0}

dirEN_train = ('/Users/maylizabeth/Desktop/ml/EN/train')
dirEN_in = ('/Users/maylizabeth/Desktop/ml/EN/dev.in')
dirEN_out = ('/Users/maylizabeth/Desktop/ml/EN/dev.out')
dirEN_test = ('/Users/maylizabeth/Desktop/ml/EN/modified_file.txt')



def get_data(data):
    raw_data = open(data, 'r',
                    encoding="utf8")  # r+ is Special read and write mode, which is used to handle both actions when working with a file
    d = raw_data.read()
    words = d.split('/n')
    return words

def emission_par(words):
    global ggdict
    global nesteddict

    totalcountBpos = 0
    totalcountBneg = 0
    totalcountBneu = 0
    totalcountIpos = 0
    totalcountIneg = 0
    totalcountIneu = 0
    totalcountO = 0
    for words2 in words:
        globaldict = {}
        words3 = words2.split('\n')  ##words3 is a list of pairs of words and their labels
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

        # Calculating the emission parameters
        for word, tagdict in ggdict.items():
            for tag, count in tagdict.items():
                if tag == 'B-positive':
                    ggdict[word][tag] = ggdict[word][tag] / totalcountBpos
                elif tag == 'B-negative':
                    ggdict[word][tag] = ggdict[word][tag] / totalcountBneg
                elif tag == 'B-neutral':
                    ggdict[word][tag] = ggdict[word][tag] / totalcountBneu
                elif tag == 'I-positive':
                    ggdict[word][tag] = ggdict[word][tag] / totalcountIpos
                elif tag == 'I-negative':
                    ggdict[word][tag] = ggdict[word][tag] / totalcountIneg
                elif tag == 'I-neutral':
                    ggdict[word][tag] = ggdict[word][tag] / totalcountIneu
                else:
                    ggdict[word][tag] = ggdict[word][tag] / totalcountO
        #print(ggdict)


# print("ggdict:%s" %ggdict)

# print(totalcountO)
# print(totalcountBpos)
# print(totalcountBneg)
# print(totalcountBneu)
# print(totalcountIpos)
# print(totalcountIneg)
# print(totalcountIneu)

def modified_test(trainfile, testfile):
    raw_train = open(trainfile, 'r+',
                     encoding="utf8")  # r+ is Special read and write mode, which is used to handle both actions when working with a file
    # d_train = raw_train.read()
    # words = d_train.split('/n')

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
    for words2 in raw_test:
        words3 = words2.rsplit()
        # print(words3)
        for i in range(len(words3)):
            key = words3[i]
            words_in_test.append(key)
    modified_test = words_in_test

    kcount = 0
    for x in range(len(words_in_test)):
        if words_in_test[x] not in words_in_train:
            modified_test[x] = '#UNK#'
            kcount += 1
    # print(modified_test)
    # print(kcount)

    f = open("modified_file.txt", "w+", encoding="utf8")
    for item in range(len(modified_test)):
        word = modified_test[item]
        f.write("%s\n" % word)
    f.close()

    return modified_test, kcount

def modified_emission_par(words,kcount):
    global ggdict
    global nesteddict

    totalcountBpos = 0
    totalcountBneg = 0
    totalcountBneu = 0
    totalcountIpos = 0
    totalcountIneg = 0
    totalcountIneu = 0
    totalcountO = 0
    for words2 in words:
        globaldict = {}
        words3 = words2.split('\n')  ##words3 is a list of pairs of words and their labels
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
        # print(ggdict)
        #countdict = {"B-positive": totalcountBpos, "B-negative": totalcountBneg}

    return ggdict

#initialise emission params
modified_test, kcount = modified_test(dirEN_train, dirEN_in)
emission_params = modified_emission_par(get_data(dirEN_train),kcount)
emission_params_EN=emission_params
label_count_EN=kcount
#print (emission_params)

obs=obs_final
states=state
state=("B-positive", "B-negative", "B-neutral", "I-positive", "I-negative", "I-neutral","O")
start_p= {"B-positive":1/7, "B-negative":1/7, "B-neutral":1/7, "I-positive":1/7, "I-negative":1/7, "I-neutral":1/7,"O":1/7} 
obs_final=tuple(obs)
trans_p=transition_params
emit_p=emission_params

for i in trans_p:
    

#print(trans_p)
def viterbi(obs, states, start_p, trans_p, emit_p):
    #base case
    U = [{}]
    for st in states:
        #V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
        U[0][st] = {"prob": start_p[st]*emit_p[st][obs[0]]}
        print(U)

U=[]
S = []
for i in state:
    if 'START' in trans_p[i]:
        U.append(trans_p[i]['START'])
        S.append(i)
    else:
        trans_p[i]['START']=0
        U.append(trans_p[i]['START'])
        S.append(i)
for x in range(len(S)):
    
 
    
        
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)
            for prev_st in states:
                if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * emit_p[obs][state[t]]
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
    #print(V)
    
    for line in dptable(V):
        print (line)
    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
        
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    return ('The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' %max_prob)

def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)
     

#a=viterbi(obs,states,start_p,trans_p,emit_p)
#print()
