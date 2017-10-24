#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 22:43:06 2017

@author: shutao
"""

import re
from sklearn.svm import SVC

class utility():
    
    
    
    
    # train SVM 
    # input: vectors tfidf, data, parameter for C, gamma and kernel
    # output: svm model
    def train_svm(self, vectors, data, c_value, gamma_value, kernel_type):
        svm = SVC(C=c_value, gamma=gamma_value, kernel=kernel_type)
        svm.fit(vectors, data)
        return svm
    
    
    
    
    
    def neg_tag(text):
    transformed = re.sub(r"\b(?:never|nothing|nowhere|noone|none|not|haven't|hasn't|hasnt|hadn't|hadnt|can't|cant|couldn't|couldnt|shouldn't|shouldnt|won't|wont|wouldn't|wouldnt|don't|dont|doesn't|doesnt|didn't|didnt|isnt|isn't|aren't|arent|aint|ain't|hardly|seldom)\b[\w\s]+[^\w\s]", lambda match: re.sub(r'(\s+)(\w+)', r'\1NEG_\2', match.group(0)), text, flags=re.IGNORECASE)
    return(transformed)