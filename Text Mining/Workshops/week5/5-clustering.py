
# coding: utf-8

# In[4]:


# In this workshop we perform document clustering using sklearn

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# We are using the subnews dataset that we used last week. 
# The "Class" labels here are only used for sanity check of the clusters found later.
# Remember, in actual use of document clustering, the documents DON'T come with labeled classes.
# It's unsupervised learning.

import pandas as pd
news=pd.read_table('r8-train-all-terms.txt',header=None,names = ["Class", "Text"])
subnews=news[(news.Class=="trade")| (news.Class=='crude')|(news.Class=='money-fx') ]
subnews.head()


# In[12]:


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
    text_after_process=" ".join(tokens)
    return(text_after_process)

# Apply preprocessing to every document in the training set.
text = subnews['Text']
toks = text.apply(pre_process)


# In[13]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline


# In[14]:


# Create tfidf matrix
vectorizer = TfidfVectorizer(max_df=0.7, max_features=2500,
                             min_df=3, stop_words=mystopwords,
                             use_idf=True)
X = vectorizer.fit_transform(toks)
X.shape


# In[47]:


# Use SVD to reduce dimensions
svd = TruncatedSVD(50)
normalizer = Normalizer(copy=False)
lsa = make_pipeline(svd, normalizer)
X_lsa = lsa.fit_transform(X)


# In[48]:


# Check how much variance is explained
explained_variance = svd.explained_variance_ratio_.sum()
print("Explained variance of the SVD step: {}%".format(int(explained_variance * 100)))


# In[49]:


# Now the actual clustering
from sklearn.cluster import KMeans

km3 = KMeans(n_clusters=3, init='k-means++', max_iter=100, n_init=1)
get_ipython().magic('time km3.fit(X_lsa)')


# In[50]:


# How do we know the clustering result is good or not?
# If we have labels available, we can use this to derive how coherent the clusters are.
# Homogeneity: each cluster contains only members of a single class

from sklearn import metrics

labels = subnews['Class']
print("Homogeneity for 3 clusters: %0.3f" % metrics.homogeneity_score(labels, km3.labels_))
# K means start from different random starting point.

# In[51]:


# Let's try some other K values to compare their metrics
km2 = KMeans(n_clusters=2, init='k-means++', max_iter=100, n_init=1)
get_ipython().magic('time km2.fit(X_lsa)')

km4 = KMeans(n_clusters=4, init='k-means++', max_iter=100, n_init=1)
get_ipython().magic('time km4.fit(X_lsa)')

km5 = KMeans(n_clusters=5, init='k-means++', max_iter=100, n_init=1)
get_ipython().magic('time km5.fit(X_lsa)')


# In[52]:


# What are their homogeneity scores?
print("Homogeneity for 2 clusters: %0.3f" % metrics.homogeneity_score(labels, km2.labels_))
print("Homogeneity for 4 clusters: %0.3f" % metrics.homogeneity_score(labels, km4.labels_))
print("Homogeneity for 5 clusters: %0.3f" % metrics.homogeneity_score(labels, km5.labels_))


# In[53]:


# Completeness: all members of a given class are assigned to the same cluster

print("Completeness for 2 clusters: %0.3f" % metrics.completeness_score(labels, km2.labels_))
print("Completeness for 3 clusters: %0.3f" % metrics.completeness_score(labels, km3.labels_))
print("Completeness for 4 clusters: %0.3f" % metrics.completeness_score(labels, km4.labels_))
print("Completeness for 5 clusters: %0.3f" % metrics.completeness_score(labels, km5.labels_))


# In[54]:


# Silhouette: more similar within clusters, more distant between clusters
# The higher the better
print("Silhouette Coefficient for 2 clusters: %0.3f"
      % metrics.silhouette_score(X_lsa, km2.labels_))
print("Silhouette Coefficient for 3 clusters: %0.3f"
      % metrics.silhouette_score(X_lsa, km3.labels_))
print("Silhouette Coefficient for 4 clusters: %0.3f"
      % metrics.silhouette_score(X_lsa, km4.labels_))
print("Silhouette Coefficient for 5 clusters: %0.3f"
      % metrics.silhouette_score(X_lsa, km5.labels_))


# In[61]:


# We still need to see the more representative words for each cluster to understand them.

def print_terms(cm, num):
    original_space_centroids = svd.inverse_transform(cm.cluster_centers_)
    order_centroids = original_space_centroids.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(num):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()


# In[62]:


# Print the terms for the 2-cluster model
print_terms(km2, 2)


# In[63]:


print_terms(km3, 3)


# In[64]:


print_terms(km4, 4)


# In[65]:


print_terms(km5, 5)


# In[70]:


# Let's map the cluster label to the categories to see where is the confusion

dict = {2: 'crude', 1: 'money-fx', 0: 'trade'}
cluster_labels = [ dict[c] for c in km3.labels_]


# In[71]:


import numpy as np
print(metrics.confusion_matrix(cluster_labels, labels))
print(np.mean(cluster_labels == labels) )
print(metrics.classification_report(cluster_labels, labels))


# In[ ]:




