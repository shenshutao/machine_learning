#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 15:58:18 2017

@author: shutao
"""
import pandas as pd
import nltk

from wordcloud import WordCloud
import matplotlib.pyplot as plt

human_body_dictionary = ['head','brain','arm','back','waist','buttocks / backside',
                         'leg','face','chest','stomach','abdomen','hip','hand','foot',
                         'eye','nose','mouth','chin','hair','ear','lips','neck',
                         'nail','thumb','finger','wrist','palm','shoulder',
                         'arm','elbow','knee','thigh','shin','calf','ankle','heel','toe','feet']

WNlemma = nltk.WordNetLemmatizer()

def preprocess_tokenize_body(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens=[WNlemma.lemmatize(t) for t in tokens]
    tokens=[word for word in tokens if word in human_body_dictionary]
    text_after_process=" ".join(tokens)
    return(text_after_process)
    
osha_data = pd.read_csv("result/osha_q1_q2.csv")

summary_data_combine = " ".join(osha_data['Case Summary'])

tokenized_data_series = preprocess_tokenize_body(summary_data_combine)

# Generate a word cloud image
wc = WordCloud(background_color="white").generate(tokenized_data_series)

plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.savefig('result/body_parts.png')
plt.close()
