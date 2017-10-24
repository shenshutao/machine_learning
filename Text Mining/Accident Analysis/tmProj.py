#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 17:32:23 2017

@author: shutao
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# change working directory
os.chdir('/Users/shutao/Desktop/Text Mining/Project')

# load data
msia_data = pd.read_csv("MsiaAccidentCases.csv")

print(msia_data.shape)
categories  = msia_data['Cause '].unique()
print(categories)

# split data
X_train, X_test, y_train, y_test = train_test_split(msia_data['Summary Case'], msia_data['Cause '], test_size=0.33)

# train SVM
vectorizer = TfidfVectorizer()
X_train_vectors = vectorizer.fit_transform(X_train)
svm = SVC(C=1000.0, gamma='auto', kernel='rbf')
svm.fit(X_train_vectors, y_train)

X_test_vectors = vectorizer.transform(X_test)
predSVM = svm.predict(X_test_vectors)
y_test_pred = list(predSVM)


print(classification_report(y_test, y_test_pred))
print(accuracy_score(y_test, y_test_pred))
print(confusion_matrix(y_test, y_test_pred))



