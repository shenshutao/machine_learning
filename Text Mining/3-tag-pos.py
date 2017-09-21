# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 00:19:41 2017
Workshop: IE - POS Tagging
@author: issfz
"""

import nltk
from nltk import word_tokenize, pos_tag

# ===== POS Tagging using NLTK =====

sent = '''Professor Tan Eng Chye, NUS Deputy President and Provost, and Professor 
Menahem Ben-Sasson, President of HUJ signed the joint degree agreement at NUS, 
in the presence of Ambassador of Israel to Singapore Her Excellency Amira Arnon 
and about 30 invited guests, on July 03, 2013.
'''

# The input for POS tagger needs to be tokenized first.
sent_pos = pos_tag(word_tokenize(sent))
sent_pos

# A more simplified tagset - universal
sent_pos2 = pos_tag(word_tokenize(sent), tagset='universal')
sent_pos2

# The wordnet lemmatizer works properly with the pos given
wnl = nltk.WordNetLemmatizer()
wnl.lemmatize('signed', pos = 'v')

#------------------------------------------------------------------------
# Exercise: remember the wordcloud we created last week? Now try creating 
# a wordcloud with only nouns, verbs, adjectives, and adverbs, with nouns 
# and verbs lemmatized.
#-------------------------------------------------------------------------