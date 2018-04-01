
# coding: utf-8

# In[62]:


# In this workshop we perform topic modeling using gensim

# We are using the subnews dataset that we used last week. 
# The "Class" labels here are only used for sanity check of the topics discovered later.
# Remember, in actual use of topic modelling, the documents DON'T come with labeled classes.
# It's unsupervised learning.

import pandas as pd
news=pd.read_table('r8-train-all-terms.txt',header=None,names = ["Class", "Text"])
subnews=news[(news.Class=="trade")| (news.Class=='crude')|(news.Class=='money-fx') ]
subnews.head()


# In[99]:


# Let's use the similar preprocessing we used last week.
# The output of each document is a list of tokens.

import nltk
from nltk.corpus import stopwords
mystopwords=stopwords.words("English") + ['one', 'become', 'get', 'make', 'take']
WNlemma = nltk.WordNetLemmatizer()

def pre_process(text):
    tokens = nltk.word_tokenize(text)
    tokens=[ WNlemma.lemmatize(t.lower()) for t in tokens]
    tokens=[ t for t in tokens if t not in mystopwords]
    tokens = [ t for t in tokens if len(t) >= 3 ]
    return(tokens)


# In[102]:


#split the data into training and testing
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(subnews.Text, subnews.Class, test_size=0.33, random_state=12)


# In[103]:


# Apply preprocessing to every document in the training set.
toks_train = X_train.apply(pre_process)


# In[66]:


import logging
import gensim 
from gensim import corpora

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# In[104]:


# Prepare a vocabulary dictionary.
dictionary = corpora.Dictionary(toks_train)
print(dictionary)


# In[105]:


# It's mappings between ids and tokens
# To get a token's id
dictionary.token2id['exchange']


# In[106]:


# To get the token of an id
dictionary[157]


# In[107]:


# Filter off any words with document frequency less than 3, or appearing in more than 80% documents
dictionary.filter_extremes(no_below=3, no_above=0.7)
print(dictionary)


# In[108]:


# Use the dictionary to prepare a DTM (using TF)
dtm_train = [dictionary.doc2bow(d) for d in toks_train ]
# doc 2 bag of words


# In[109]:


# Build an LDA model for 3 topics out of the DTM
get_ipython().magic('time lda = gensim.models.ldamodel.LdaModel(dtm_train, num_topics = 3, id2word = dictionary, passes = 100)')


# In[110]:


# To see the topics, with the most probable words in each topic. What topics to you see? 
lda.show_topics()


# In[111]:


# You can also request to see more words per topic
lda.show_topics(num_words=20)


# In[41]:


# A similar function showing each topic with its most probable words and its topic coherence score
lda.top_topics(dtm_train)


# In[112]:


# We can therefore derive the average topic coherence, as a way to evaluate the topic models
import numpy as np
lda_coherence = [ n for _, n in lda.top_topics(dtm_train) ]
np.mean(lda_coherence)


# In[113]:


# Another metric for gauging goodness of models, perplexity, is accessed using bound() function
lda.bound(dtm_train)


# In[114]:


# Get the topic distribution of documents
dtopics_train = lda.get_document_topics(dtm_train)


# In[122]:


# Get the topic likelihood for the first document in train set
for i in range(0, 5):
    print(dtopics_train[i])


# In[123]:


# Pick the topic with the highest probability for each document, map it to the label
# NOTE: the mapping may change in a different run
from operator import itemgetter
top_train = [ max(t, key=itemgetter(1))[0] for t in dtopics_train ]
dict = {1: 'crude', 0: 'money-fx', 2: 'trade'}
topic_train = [ dict[t] for t in top_train ]


# In[124]:


# Now let's see how well these topics match the actual categories

from sklearn import metrics
print(metrics.confusion_matrix(topic_train, y_train))
print(np.mean(topic_train == y_train) )
print(metrics.classification_report(topic_train, y_train))


# In[125]:


# The typical practice is to use the reserved test set for evaluation
toks_test = X_test.apply(pre_process)
dtm_test = [dictionary.doc2bow(d) for d in toks_test ]
dtopics_test = lda.get_document_topics(dtm_test)
top_test = [ max(t,key=itemgetter(1))[0] for t in dtopics_test ]
topic_test = [ dict[t] for t in top_test ]
print(metrics.confusion_matrix(topic_test, y_test))
print(np.mean(topic_test == y_test) )
print(metrics.classification_report(topic_test, y_test))


# In[128]:


# In actual use case, we wouldn't have class labels for comparison.
# So mean topic coherence and model perplexity can be checked.
test_coherence = [ n for _, n in lda.top_topics(dtm_test) ]
np.mean(test_coherence)


# In[129]:


lda.bound(dtm_test)


# In[130]:


# Different models can be compared using such metrics

get_ipython().magic('time lda4 = gensim.models.ldamodel.LdaModel(dtm_train, num_topics = 4, id2word = dictionary, passes = 20)')


# In[132]:


lda4.show_topics()


# In[133]:


test_coherence4 = [ n for _, n in lda4.top_topics(dtm_test) ]
np.mean(test_coherence4)


# In[134]:


get_ipython().magic('time lda2 = gensim.models.ldamodel.LdaModel(dtm_train, num_topics = 2, id2word = dictionary, passes = 20)')
lda2.show_topics()


# In[135]:


test_coherence2 = [ n for _, n in lda2.top_topics(dtm_test) ]
np.mean(test_coherence2)


# In[136]:


get_ipython().magic('time lsi = gensim.models.LsiModel(dtm_train, id2word=dictionary, num_topics=200)')


# In[137]:


lsi.print_topics(5)


# In[138]:


lsi_test = lsi[dtm_test]


# In[139]:


lsi_test[0]


# In[ ]:




