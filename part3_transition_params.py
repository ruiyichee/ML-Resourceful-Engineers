#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 11:29:59 2018

@author: maylizabeth
"""

EN_train = ('/Users/maylizabeth/Desktop/machine learning/EN/train')

def transition_params(train_file):
    transition_count ={}
    state_count = {}
    u_state = 'START'
    v_state = 'STOP'

    state_count[u_state] = 0
    state_count[v_state] = 0
    transition_count[v_state] = {}

    with open(EN_train, encoding='utf=8') as file:
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


transition_params_EN = transition_params(EN_train)
print (transition_params_EN)





