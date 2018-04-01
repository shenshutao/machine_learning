#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 20:24:54 2017

@author: shutao
"""

## only 
##from nltk.corpus import reuters
#import nltk
#from nltk import word_tokenize, pos_tag
#import simplejson as json
#
## Or open the JSON data file from your current working directory
#data =  open("Article_1.json", "r")
#
## Load in the JSON object in the file
#jdata = json.load(data)
#
#text=jdata['Text']
#
#tag_pos = pos_tag(word_tokenize(text))
#tag_pos[:10]
#
#wnl = nltk.WordNetLemmatizer()
#token_required = [wnl.lemmatize(t[0], pos='v') for t in tag_pos if t[1] in ('ADJ','ADV') ] + [t[0] for t in tag_pos if t[1] in ('NN','VBP')]
#
#
##ldc pos tag
#
#text_clean=" ".join(token_required)

text_clean2 = "Customer Implimentation|Customer Implimentation|Customer Implimentation|Visa|Mastercard"

import wordcloud
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

wc = WordCloud(background_color="white", regexp=r"[a-zA-Z ]+", normalize_plurals=False, collocations=False).generate(text_clean2)

# Display the generated image:
# the matplotlib way:

plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()
