#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 22:43:06 2017

@author: shutao
"""

import nltk
import string
import pandas as pd

from nltk.corpus import stopwords

import matplotlib.pyplot as plt
from collections import Counter
from nltk.stem.porter import PorterStemmer
        
def word_feats(words):
    return dict([(word, True) for word in words])

# stopwords removal
newstopwords=stopwords.words("English") + ['died','die','kill','death','work', 'employe', 'is','\'s']
WNlemma = nltk.WordNetLemmatizer()
porter_stemmer = PorterStemmer()
    
def pre_process(text):
    text = text.lower() 
    tokens = nltk.word_tokenize(text)
    tokens=[porter_stemmer.stem(t) for t in tokens]
    tokens=[WNlemma.lemmatize(t) for t in tokens]
    tokens=[word for word in tokens if word not in newstopwords]
    tokens=[word for word in tokens if word not in set(string.punctuation)]
    text_after_process=" ".join(tokens)
    return(text_after_process)
    
def preprocess_tokenize(text):
    tokens = nltk.word_tokenize(text)
    text_after_process=" ".join(tokens)
    return(text_after_process)

def show_most_informaitive_terms(feature_names, nbclf):
    categorylist = list(nbclf.classes_)
    cate_feat_table = {}
    for category in categorylist:
        sortn = sorted(zip(nbclf.coef_[categorylist.index(category)], feature_names), reverse=True)
# =============================================================================
#         print('For category: \'',category,'\', the most important features are: ')
#         {print(' ', feat, '{0:.2f}'.format(float(coef))) for coef, feat in sortn[:10]}
# =============================================================================
        cate_list = []
        {cate_list.append(feat) for coef, feat in sortn[:10]}
        cate_feat_table[category] = []
        cate_feat_table[category] = cate_list
    
    print(pd.DataFrame(cate_feat_table))
        
        

def predict_with_threshold(nb_clf, inputdata, threshold):
    predict_probabilities = nb_clf.predict_proba(inputdata)
    categorylist = list(nb_clf.classes_)
    
    result = []
    for i in range(0, len(predict_probabilities)):
        a=list(predict_probabilities[i])
        maxindex = a.index(max(a))
    
        if predict_probabilities[i][maxindex] >= threshold:
            result.append(categorylist[maxindex])
        else:
            result.append('Others')
            
    return(result)

def hist_list_categories(listdata, graph_name):
    categories_count = Counter(listdata)
    df = pd.DataFrame.from_dict(categories_count, orient='index')
    df.plot(kind='barh')
    plt.savefig(graph_name)
    plt.close()

# print(pre_process('Died being crushed by truck exploding explosion'))

#print('{0:.2f}'.format(float('3.14159')))

def calc_precision_from_confusion_matrix(cm):
    correctList = [cm[i][i] for i in range(0,len(cm))]
    correct_cm = sum(correctList)
    all_cm = sum(sum(cm))
    return(correct_cm/all_cm)
    