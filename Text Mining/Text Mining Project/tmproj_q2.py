#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 15:58:18 2017

@author: shutao
"""
import nltk
import string

import pandas as pd
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# stopwords removal
newstopwords=stopwords.words("English")
WNlemma = nltk.WordNetLemmatizer()
    
def pre_process(text):
    text = text.lower() 
    tokens = nltk.word_tokenize(text)
    tokens=[WNlemma.lemmatize(t) for t in tokens]
    tokens=[word for word in tokens if word not in newstopwords]
    tokens=[word for word in tokens if word not in set(string.punctuation)]
    return(tokens)

occupations_dict = pd.read_json('occupations/construction_major_occupations.json', typ='series')

# step1: if the occupation name is exist directly in the text.
def find_occupation_step1(text):
    for occupation in occupations_dict['occupations']:
            if occupation['name'] in text:
                return occupation['name']

# step2: find occupation with the related words.
def find_occupation_step2(text):
    target_tokens = pre_process(text)
    points_list = []
    for occupation in occupations_dict['occupations']:
        points = 0
        for token in target_tokens:
            if token in occupation['related_words']:
                points += 1
        points_list.append(points)
    # return the first max point
    if max(points_list) > 0:
        return occupations_dict['occupations'][points_list.index(max(points_list))]['name']

# =============================================================================
# Main
# =============================================================================
# Load data
osha_data = pd.read_csv("result/osha_q1.csv")

combine = osha_data['Case Details'] + osha_data['Case Summary']

occupation_pred = []

# Predict occupation
for text in combine:
    if text:
        #step 1
        step1_pred = find_occupation_step1(text)

        if step1_pred:
            occupation_pred.append(step1_pred)
        else:
            #step 2
            occupation_pred.append(find_occupation_step2(text))
 

# Save into file
osha_data['Occupation_Pred'] = occupation_pred
osha_data.to_csv('result/osha_q1_q2.csv')

# Genarate word cloud
tokenized_data = " ".join(filter(None, occupation_pred))
wc = WordCloud(background_color="white").generate(tokenized_data)

plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.savefig('result/occupation.png')
plt.close()
