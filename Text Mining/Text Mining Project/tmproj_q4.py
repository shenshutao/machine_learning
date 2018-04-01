#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 18:09:15 2017

@author: shutao
"""
import string
import nltk

import pandas as pd
from nltk import word_tokenize, pos_tag

import matplotlib.pyplot as plt

from utility import *

# load data
osha_data = pd.read_csv("result/osha_q1_q2.csv")
        
# =============================================================================
# ('was', 'VBD'), ('operating', 'VBG'), ('a', 'DT'), ('wire', 'NN'),
#  ('rope', 'NN'), ('winding', 'VBG'), ('machine', 'NN'), ('.', '.')
# =============================================================================

# Pattern: first sentence .was + VBG till puncation (together with Date?)
def get_activity(text):
    nltk_pos = pos_tag(word_tokenize(text))
    for index in range(0, len(nltk_pos)):
        if nltk_pos[index][0] == 'was':
            if nltk_pos[index+1][1] == 'VBG':
                activity = []
                for i in range(index+1, len(nltk_pos)):
                    if nltk_pos[i][1] in set(string.punctuation):
                        break
                    else:
                        activity.append(nltk_pos[i][0])
     
                return " ".join(activity)
            

osha_data['Activity'] = osha_data['Case Details'].apply(get_activity)

osha_data.to_csv('result/osha_q1_q2_q4.csv')

from wordcloud import WordCloud
from nltk.corpus import stopwords

newstopwords=stopwords.words("English") + ['working','operating', 'using','employee','worker', 'truck','coworker']

WNlemma = nltk.WordNetLemmatizer()
def preprocess_tokenize_body(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens=[word for word in tokens if word not in newstopwords]
    tokens=[WNlemma.lemmatize(t) for t in tokens]
    text_after_process=" ".join(tokens)
    return(text_after_process)

tokenize_data_combine = " ".join(filter(None, osha_data['Activity']))

tokenized_data_series = preprocess_tokenize_body(tokenize_data_combine)

# Generate a word cloud image
wc = WordCloud(background_color="white").generate(tokenized_data_series)

plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.savefig('result/activities.png')
plt.close()



