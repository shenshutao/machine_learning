#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:55:24 2017

@author: shutao
"""
import os
import pickle as pk
import pandas as pd
import time
import numpy

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from collections import Counter

import nltk
from nltk.classify import NaiveBayesClassifier, MaxentClassifier
from nltk import word_tokenize as wt

import matplotlib.pyplot as plt

from utility import pre_process, word_feats

# change working directory
os.chdir('/Users/shutao/Desktop/Sentiment Mining/workshops/Day 2')

# load training / test set
traindata = pd.read_csv("train.csv", encoding='iso-8859-1')
testdata  = pd.read_csv("test.csv", encoding='iso-8859-1')
data =  pd.concat([traindata,testdata])

# =============================================================================
# text = pre_process("I shouldn't like that place you Keep Calling awesome is goodness likely.")
# print(text)
# =============================================================================

categories_count = Counter(data["Sentiment"])
df = pd.DataFrame.from_dict(categories_count, orient='index')
df.plot(kind='barh')
plt.savefig('data_quality.png')
plt.close()

# notice that build SVM & Max Entropy is quite time consuming as our data is large. 
# so I mask below code.
# the code below's purpose is find the best model by cross validation approach.
# In my laptop, training time is: SVM: 137s, Naive Bayes: 1.7s, KNN: 9s, Max Entropy: 225s
# =============================================================================
# choose the best model
# =============================================================================
print('Start choosing best models...')
# =============================================================================
# 
# # pre process data
# start = time.clock()
# data['text'] = data['text'].apply(pre_process)
# elapsed = (time.clock() - start)
# print("Preprocess time used:",elapsed)
# 
# =============================================================================
# =============================================================================
# try svm
# =============================================================================
test_results = []
for lp in range(10):
    # split data
    X_train, X_test, y_train, y_test = train_test_split(data['text'], data['Sentiment'], test_size=0.3)
    
    ########################
    # train SVM
    vectorizer = TfidfVectorizer()
    X_train_vectors = vectorizer.fit_transform(X_train)
    svm = SVC(C=1000.0, gamma='auto', kernel='rbf')
    svm.fit(X_train_vectors, y_train)
    
    X_test_vectors = vectorizer.transform(X_test)
    predSVM = svm.predict(X_test_vectors)
    y_test_pred = list(predSVM)
       
    test_results.append(accuracy_score(y_test, y_test_pred))

print('Performance of SVM')
plt.boxplot(test_results)
plt.savefig('svm_performance.png')
plt.close()
print('mean is ', numpy.mean(test_results))

# =============================================================================
# try naive bayes
# =============================================================================
test_results = []
for lp in range(50):
        # split data
        X_train, X_test, y_train, y_test = train_test_split(data['text'], data['Sentiment'], test_size=0.3)
        
        ########################
        # train Naive Bayes
        nb_clf = Pipeline([('vect', CountVectorizer(binary=True)), ('clf', MultinomialNB())])
        
        nb_clf.fit(X_train,y_train)
        y_test_pred = nb_clf.predict(X_test)
        
        test_results.append(accuracy_score(y_test, y_test_pred))

print('Performance of Naive Bayes')
plt.boxplot(test_results)
plt.savefig('naive_bayes_performance.png')
plt.close()
print('mean is ', numpy.mean(test_results))


# =============================================================================
# # =============================================================================
# # try naive bayes 2
# # =============================================================================
# 
# test_results = []
# for lp in range(10):
#         # split data
#         X_train, X_test, y_train, y_test = train_test_split(data['text'], data['Sentiment'], test_size=0.3)
#         
#         ########################
#         # train Naive Bayes 2
#         trainset = zip(X_train, y_train)
#         train_tokenized = [[wt(x), c] for x,c in trainset]
#         train_featureset = [(word_feats(d), c) for (d,c) in train_tokenized]
#         
#         nb_clf2 = NaiveBayesClassifier.train(train_featureset)
#         
#         test_tokenized = [wt(x) for x in X_test]
#         test_featureset = [(word_feats(d)) for d in test_tokenized]
#         y_test_pred = nb_clf2.classify_many(test_featureset)
#                 
#         test_results.append(accuracy_score(y_test, y_test_pred))
#         print(accuracy_score(y_test, y_test_pred))
# 
# print('Performance of Naive Bayes 2')
# plt.boxplot(test_results)
# plt.savefig('naive_bayes_2_performance.png')
# plt.close()
# print('mean is ', numpy.mean(test_results))
# =============================================================================

# =============================================================================
# try knn
# =============================================================================
test_results = []
for lp in range(10):
    X_train, X_test, y_train, y_test = train_test_split(data['text'], data['Sentiment'], test_size=0.3)
    
    knn_clf = Pipeline([('vect', CountVectorizer(binary=True)), ('clf', KNeighborsClassifier())])
    knn_clf.fit(X_train,y_train)
    
    y_test_pred = knn_clf.predict(X_test)

    test_results.append(accuracy_score(y_test, y_test_pred))
 
print('Performance of KNN:')
plt.boxplot(test_results)
plt.savefig('knn_performance.png')
plt.close()
print('mean is ', numpy.mean(test_results))

# =============================================================================
# try max Ent
# =============================================================================
test_results = []
for lp in range(3):
    X_train, X_test, y_train, y_test = train_test_split(data['text'], data['Sentiment'], test_size=0.3)
    
    trainset = zip(X_train, y_train)
    train_tokenized = [[wt(x), c] for x,c in trainset]
    train_featureset = [(word_feats(d), c) for (d,c) in train_tokenized]
    
    maxent_clf = MaxentClassifier.train(train_featureset, algorithm="IIS", max_iter=2, trace=0)
    
    test_tokenized = [wt(x) for x in X_test]
    test_featureset = [(word_feats(d)) for d in test_tokenized]
    y_test_pred = maxent_clf.classify_many(test_featureset)

    test_results.append(accuracy_score(y_test, y_test_pred))

print('Performance of Max Entropy:')
plt.boxplot(test_results)
plt.savefig('max_entropy_performance.png')
plt.close()
print('mean is ', numpy.mean(test_results))

print('Multinomial Naive Bayes model give the best result.')

# =============================================================================
# after previous step, we find best model is Naive Bayes
# =============================================================================
# retrain Naive Bayes for question 1

## data pre process
print('retrain Naive Bayes for question 1')
traindata = pd.read_csv("train.csv", encoding='iso-8859-1')
testdata  = pd.read_csv("test.csv", encoding='iso-8859-1')
traindata['text_aft_preprocess'] = traindata['text'].apply(pre_process)
testdata['text_aft_preprocess'] = testdata['text'].apply(pre_process)

## build binary term‐document matrix, then build multinomial naive bayes model
nb_clf = Pipeline([('vect', CountVectorizer(binary=True)), ('clf', MultinomialNB())])

nb_clf.fit(traindata['text_aft_preprocess'],traindata['Sentiment']) 
y_test_pred = nb_clf.predict(testdata['text_aft_preprocess'])

print('Confusion Matrix:')
print(confusion_matrix(testdata['Sentiment'], y_test_pred))
print('Classification Report:')
print(classification_report(testdata['Sentiment'], y_test_pred))
print('Accuracy Score:')
print(accuracy_score(testdata['Sentiment'], y_test_pred))

print('Store test_scored.csv')
testdata = pd.read_csv("test.csv", encoding='iso-8859-1')
testdata['pred_sentiment'] = y_test_pred
testdata['text_aft_preprocess'] = testdata['text'].apply(pre_process)
testdata.to_csv('test_scored.csv')

# for question 2:
postiveIndex = list(nb_clf.named_steps['clf'].classes_).index('positive')
negativeIndex = list(nb_clf.named_steps['clf'].classes_).index('negative')
        
feature_names = nb_clf.named_steps['vect'].get_feature_names()

sortn = sorted(zip(nb_clf.named_steps['clf'].coef_[0], feature_names))
print("words link to positive reviews:")
{print(' ', feat, coef) for coef, feat in sortn[-5:]}

# =============================================================================
# sort_positivefeature = sorted(zip(nb_clf.named_steps['clf'].feature_log_prob_[postiveIndex], feature_names))
# {print('positive most prob word: ', feat, coef) for coef, feat in sort_positivefeature[-5:]}
# 
# sort_negativefeature = sorted(zip(nb_clf.named_steps['clf'].feature_log_prob_[negativeIndex], feature_names))
# {print('negative most prob word:', feat, coef) for coef, feat in sort_negativefeature[-5:]}
# =============================================================================


classifier_nb = nb_clf.named_steps['clf']
pk.dump(nb_clf, open("classifier_nb.pk","wb"))


print('''However, the most informative words above is not make sense for negative reviews, 
      so I use the nltk's naive bayes to get these words...''')

# train NLTK Naive Bayes
traindata = pd.read_csv("train.csv", encoding='iso-8859-1')
traindata['text_aft_preprocess'] = traindata['text'].apply(pre_process)

trainset = zip(traindata['text_aft_preprocess'], traindata['Sentiment'])
train_tokenized = [[wt(x), c] for x,c in trainset]
train_featureset = [(word_feats(d), c) for (d,c) in train_tokenized]

nb_clf2 = NaiveBayesClassifier.train(train_featureset)

mif = nb_clf2.most_informative_features()

print("words link to negative reviews:")
print(mif[:5])


