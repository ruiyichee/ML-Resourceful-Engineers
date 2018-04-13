#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 01:57:53 2018

@author: maylizabeth
"""

# Modified from Part 2 #
import codecs
EN_train = ('/Users/maylizabeth/Desktop/ml/EN/train')
EN_modified = ('/Users/maylizabeth/Desktop/ml/EN/modified_train')
EN_test = ('/Users/maylizabeth/Desktop/ml/EN/dev.in')
EN_output = ('/Users/maylizabeth/Desktop/ml/EN/dev.p2.out')
EN_gold = ('/Users/maylizabeth/Desktop/ml/EN/dev.out')
EN_viterbi = ('/Users/maylizabeth/Desktop/ml/EN/dev.p3.out')

def modified_training_set(train_file,modified_train_set):
    #fout=open ('modified_train_set','w')
    with open (train_file, encoding='utf-8') as file:
        tag_count={}
        modified_words=[]
        for line in file:
            pair=line.split()
            if len(line.split())!=0:
                tag=pair[0]
                observ=pair[1]
                if tag in tag_count.keys():
                    tag_count[tag]+=1
                else:
                    tag_count[tag]=1
        for tag in tag_count:
            if tag_count[tag]<3:
                modified_words.append(tag)
    with open (train_file, encoding='utf-8') as file2, codecs.open(modified_train_set, 'w', 'utf-8-sig') as fout:
        for line in file2:
            pair2=line.split()
            if len(line.split())!=0:
                word=pair2[0]
                sentiment=pair2[1]
                if word in modified_words:
                    fout.write("#UNK"+" "+sentiment+"\n")
                else:
                    fout.write(word+" "+sentiment+"\n")


def emission_params(train_file):
    with open(train_file, encoding = 'utf-8') as file:
        emission_count= {}
        label_count={}
        for line in file:
            pair = line.split()
            if len(line.split())!=0:
                #add 1 to count of (Xi, Yi)
                word = pair[0]
                sentiment = pair[1]
                if word in emission_count.keys():
                    if sentiment in emission_count[word].keys():
                        emission_count[word][sentiment] +=1
                    else:
                        sentiments = emission_count[word]
                        sentiments[sentiment] = 1
                else:
                    sentiment_count = {}
                    sentiment_count[sentiment] = 1
                    emission_count[word]=sentiment_count
    
                #add 1 to count of label Yi
                if sentiment in label_count.keys():
                    label_count[sentiment]+=1
                else:
                    label_count[sentiment]=1
        for keya in emission_count.keys():
            for keyb in emission_count[keya].keys():
                emission_count[keya][keyb]/=(label_count[keyb]+1)
        new_word = {}
        for key in label_count.keys():
            new_word[key] = 1/(label_count[key]+1)
        emission_count['#UNK#'] = new_word
       
        return (emission_count,label_count)
                          

def sentiment_analysis(test_file,output_file,emission_params, label_count):
    with open(test_file, encoding ='utf-8') as ifile, codecs.open(output_file, 'w', 'utf-8-sig') as ofile:
        for line in ifile:
            if len(line.split())!=0:
                word = line.split()[0]
                if word in emission_params.keys():
                    value = emission_params[word]
                    a = max(value,key=value.get)
                    ofile.write(word+" "+a+'\n')
                else:
                    value = emission_params['#UNK#']
                    a = max(value,key=value.get)
                    ofile.write(word+" "+a+'\n')
            else:
                ofile.write('\n')

                
modified_training_set(EN_train, EN_modified)                
emission_params_EN, label_count_EN = emission_params(EN_modified)
#print(label_count_EN)
sentiment_analysis(EN_test,EN_output,emission_params_EN, label_count_EN)

def transition_params(train_file):
    transition_count= {}
    state_count={}
    prev = 'START'
    end = 'STOP'
    state_count[prev] = 0
    state_count[end] = 0
    transition_count[end] = {}
    with open(train_file, encoding = 'utf-8') as file:    
        for line in file:
            pair = line.split()
            if len(pair)!= 0:
                sentiment = pair[1]
                # add prev to sentiment transition count
                if sentiment in transition_count.keys():
                    sentiment_list = transition_count[sentiment]
                    if prev in sentiment_list.keys():
                        sentiment_list[prev] += 1
                    else:
                        sentiment_list[prev] = 1
                else:
                    new_sentiment = {}
                    new_sentiment[prev] = 1
                    transition_count[sentiment] = new_sentiment

                # add to start and stop state counts
                if prev == 'START':
                    state_count[prev] += 1
                    state_count[end] += 1

                # add to state count  
                if sentiment in state_count.keys():
                    state_count[sentiment]+=1
                else:
                    state_count[sentiment]=1
              
                prev = sentiment

            else:
                sentiment_list = transition_count[end]
                if prev in sentiment_list.keys():
                    sentiment_list[prev] +=1
                else:
                    sentiment_list[prev] =1   
                prev = 'START'
    for V in transition_count.keys():
        for U in transition_count[V].keys():
            transition_count[V][U] /= state_count[U]
    return transition_count


transition_params_EN = transition_params(EN_train)
print (transition_params_EN)

def viterbi_algo(test_file, output_file, transition_params, emission_params, labels):
    sentences = []

    #with open(test_file, encoding ='utf-8') as ifile, codecs.open(output_file, 'w', 'utf-8-sig') as ofile:
    with open(EN_test, encoding ='utf-8') as ifile, codecs.open(EN_viterbi, 'w', 'utf-8-sig') as ofile:
        sentence = []
        for line in ifile:
            if len(line.split())!=0:
                sentence.append(line.split()[0])
          
            else:
                sentences.append(sentence)
                sentence = []
        
        for s in sentences:
            nodes = calculate_node_scores(s,transition_params, emission_params, labels)
            labelled_sentence = backtracking(s,nodes)
            for word in labelled_sentence:
                ofile.write(word+'\n')
            ofile.write("\n")

        
def calculate_node_scores(s, transition_params, emission_params, labels):
    nodes = {}
    #base case
    nodes[0] = {'START':[1,'nil']}
    #recursive
    for k in range (1, len(s)+1): #for each word
        X = s[k-1]
        for V in labels.keys(): #for each node
            prev_nodes_dict = nodes[k-1] #access prev nodes
            highest_score = 0
            parent = 'nil'
            #emission params
            if X in emission_params.keys():
                emission_labels = emission_params[X]

                if V in emission_labels:
                    b = emission_labels[V]
                else:
                    b = 0
            else:
                b = emission_params['#UNK#'][V]  
                
            for U in prev_nodes_dict.keys():
                #transitionparams
                prev_states = transition_params[V]
                if U in prev_states.keys():
                    a = prev_states[U]
                else:
                    a = 0
                
                #prev node score
                prev_score = prev_nodes_dict[U][0]
                score = prev_score*a*b
                
                if score>= highest_score:
                    highest_score = score
                    parent = U
            if k in nodes.keys():
                nodes[k][V] = [highest_score,parent]
            else:
                new_dict = {V:[highest_score,parent]}
                nodes[k] = new_dict
            
    #end case
    prev_nodes_dict = nodes[len(s)]
    highest_score = 0
    parent = 'nil'
    for U in prev_nodes_dict.keys():
        #transition
        prev_states = transition_params['STOP']
        if U in prev_states.keys():
            a = prev_states[U]
        else:
            a = 0
        #prev node score
        prev_score = prev_nodes_dict[U][0]
        score = prev_score*a
        if score>= highest_score:
            highest_score = score
            parent = U
    indiv_node = {'STOP': [highest_score,parent]}
    nodes[len(s)+1]=indiv_node

    return nodes

s=['mama']
nodes=[{'STOP':0.7,'tata':0.3},{'STOP':0.4,'tata':0.6},{'STOP':0.7,'tata':0.3}]
def backtracking(s, nodes):
    prev_state = 'STOP'
    for i in range(len(s)+1, 1,-1):
        prev_node = nodes[i][prev_state] 
        print(prev_node)
        prev_state = prev_node[1]
        print(prev_node[3])
        print(prev_state)
        s[i-2] += " "+prev_state
    return s
print(backtracking(s,nodes))

viterbi_algo(EN_test, EN_viterbi, transition_params_EN, emission_params_EN, label_count_EN)