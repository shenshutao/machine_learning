#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 22:51:09 2017

@author: shutao
"""

from nltk.corpus import stopwords
import re
import nltk
import string

# stopwords removal
newstopwords=stopwords.words("English") + ['\'s','was']

# negation
def neg_tag(text):
    transformed = re.sub(r"\b(?:n't|never|nothing|nowhere|noone|none|not|haven't|hasn't|hasnt|hadn't|hadnt|can't|cant|couldn't|couldnt|shouldn't|shouldnt|won't|wont|wouldn't|wouldnt|don't|dont|doesn't|doesnt|didn't|didnt|isnt|isn't|aren't|arent|aint|ain't|hardly|seldom)\b[\w\s]+[^\w\s]", lambda match: re.sub(r'(\s+)(\w+)', r'\1NEG_\2', match.group(0)), text, flags=re.IGNORECASE)
    return(transformed)

WNlemma = nltk.WordNetLemmatizer()

# =============================================================================
# data pre process: 1. lowercase 2. tokenize 3. lemmatize 4. stopword removal 5. neg tag add
# =============================================================================
def pre_process(text):
    text = text.lower() 
    text = neg_tag(text)
    tokens = nltk.word_tokenize(text)
    tokens=[word for word in tokens if word not in newstopwords]
    tokens=[WNlemma.lemmatize(t) for t in tokens]
    tokens=[word for word in tokens if word not in set(string.punctuation)]
    text_after_process=" ".join(tokens)
    return(text_after_process)

def word_feats(words):
    return dict([(word, True) for word in words])