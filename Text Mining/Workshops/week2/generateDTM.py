# -*- coding: utf-8 -*-
"""
Workshop: Text Preparation (TDM)
Created on Wed Sep  6 16:19:52 2017
@author: Fan Zhenzhen
"""
from nltk.corpus import reuters
from nltk import FreqDist
import string
from nltk.corpus import stopwords

# We'll use the reuters corpus in NLTK.
# The same steps of preprocessing can be done on documents read in from external files.

# How many files are there in the corpus?
# What are their categories? Single or multiple categories for one file?
len(reuters.fileids())
cats = [ reuters.categories(f) for f in reuters.fileids() ]
#cats[0]
#cats[:10]

cat_num = [ len(c) for c in cats ]
fd_num = FreqDist(cat_num)
fd_num.plot()


# How many documents are there in each category?
# FreqDist() can be used to find the answer, but we need to flatten the list of categories first.
cats_flat = [ c for l in cats for c in l ]
fd_cat = FreqDist(cats_flat)
fd_cat
fd_cat.most_common(20)

# Let's pick two categories and visualize the articles in each category using word cloud
grain = reuters.fileids('grain')
trade = reuters.fileids('trade')

grain_tok = [ reuters.words(f) for f in grain ] #! retrive all the tokens
trade_tok = [ reuters.words(f) for f in trade ] 

#grain_tok[:3]
#trade_tok[:3]

#Let's define a function preprocess() to perform the preprocessing steps given a file (token list):
#   punctuation removal, case lowering, stopword removal, 
#   stemming/lemmatization, further cleaning
stop = stopwords.words('english')
snowball = nltk.SnowballStemmer('english')
#wnl = nltk.WordNetLemmatizer()

def preprocess(toks):
    toks = [ t.lower() for t in toks if t not in string.punctuation ]
    toks = [t for t in toks if t not in stop ]
    toks = [ snowball.stem(t) for t in toks ]
#    toks = [ wnl.lemmatize(t) for t in toks ]
    toks_clean = [ t for t in toks if len(t) >= 3 ]
    return toks_clean

# Preprocess each file in each category
grain_clean = [ preprocess(f) for f in grain_tok ]
trade_clean = [ preprocess(f) for f in trade_tok ]

# Flatten the list of lists for FreqDist
grain_flat = [ c for l in grain_clean for c in l ]
trade_flat = [ c for l in trade_clean for c in l ]

fd_grain = FreqDist(grain_flat)
fd_trade = FreqDist(trade_flat)

# Generate word clouds for the two categories.
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wc_grain = WordCloud(background_color="white").generate_from_frequencies(fd_grain)
plt.imshow(wc_grain, interpolation='bilinear')
plt.axis("off")
plt.show()

wc_trade = WordCloud(background_color="white").generate_from_frequencies(fd_trade)
plt.imshow(wc_trade, interpolation='bilinear')
plt.axis("off")
plt.show()

# Finally, how to generate TDM

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# sklearn requires the input to be text string
grain_text = [ ' '.join(f) for f in grain_clean ]

# Create a matrix using term frequency first using CountVectorizer
# The result is in sparse matrix format
vec_tf = CountVectorizer()
grain_tf = vec_tf.fit_transform(grain_text)
grain_tf

# Where are the columns and rows then?
vec_tf.get_feature_names()
grain_tf_m = grain_tf.toarray()

vec_tf_2 = CountVectorizer(min_df = 2)
grain_tf_2 = vec_tf_2.fit_transform(grain_text)
grain_tf_2

# To have binary indexing, set "binary=True"
vec_bin = CountVectorizer(binary=True)
grain_bin = vec_bin.fit_transform(grain_text)
grain_bin.toarray()[:10]

# And tfidf indexing
vec_tfidf = TfidfVectorizer(min_df = 2)
grain_tfidf = vec_tfidf.fit_transform(grain_text)
grain_tfidf
grain_tfidf.toarray()[:10]

# To save the vectorized results for future use (save time)
import pickle
pickle.dump(grain_tfidf, open("tfidf.pkl", "wb"))
pickle.dump(vec_tfidf.vocabulary_, open("feature.pkl","wb"))
#load the content
loaded_vec = TfidfVectorizer(decode_error="replace",vocabulary=pickle.load(open("feature.pkl", "rb")))
tfidf = pickle.load(open("tfidf.pkl", "rb" ) )
tfidf
