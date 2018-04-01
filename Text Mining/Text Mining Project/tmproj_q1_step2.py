#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 17:32:23 2017

@author: shutao
"""
import pandas as pd
import numpy as np

from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.preprocessing import Binarizer
from sklearn.neighbors import KNeighborsClassifier

from nltk import MaxentClassifier
from nltk.tokenize import word_tokenize as wt

from utility import *


# load data
msia_data = pd.read_csv("msia_edit.csv")

print(msia_data.shape)
categories  = msia_data['Cause'].unique()
print(categories)

categories_count = Counter(msia_data['Cause'])
df = pd.DataFrame.from_dict(categories_count, orient='index')
df.plot(kind='barh')
plt.show()
plt.close()

###############
# remove all others cases first
msia_data = msia_data[msia_data['Cause'] != 'Others']

# =============================================================================
# data pre processing
# =============================================================================
msia_title_case = msia_data['Title Case']
msia_category = msia_data['Cause']

msia_title_case = msia_title_case.apply(pre_process)

test_results = []
for lp in range(100):
    # split data
    X_train, X_test, y_train, y_test = train_test_split(msia_title_case, msia_category, test_size=0.3)
    
    # train Multinomial Naive Bayes
    nb_clf = Pipeline([('vect', CountVectorizer()), ('binarizer', Binarizer()), ('clf', MultinomialNB(fit_prior=False))])
    nb_clf.fit(X_train,y_train )
    y_test_pred = predict_with_threshold(nb_clf, X_test, 0.6)
    
    cm = confusion_matrix(y_test, y_test_pred, labels=list(y_test.unique()))
    precision = calc_precision_from_confusion_matrix(cm)
    test_results.append(precision)
print('Performance of My Naive Bayes')
plt.boxplot(test_results)
plt.savefig('result/q1_step2_model_precision.png')
plt.close()
print('mean is ', np.mean(test_results))


print('=========================== step 12===========================================')
# train Multinomial Naive Bayes
nb_clf = Pipeline([('vect', CountVectorizer(binary = True)), ('clf', MultinomialNB(fit_prior=False))])
nb_clf.fit(msia_title_case, msia_category)
# manually check if the most informative terms make sense in step 1
show_most_informaitive_terms(nb_clf.named_steps['vect'].get_feature_names(), nb_clf.named_steps['clf'])

osha_data = pd.read_csv("result/osha_q1_step1.csv")
osha_data['Title Case Aft'] = osha_data['Case Title'].apply(pre_process)

step2_pred = predict_with_threshold(nb_clf,osha_data['Title Case Aft'], 0.6)

# the records in Others is too many in step 1
result = filter(lambda a: a != 'Others', step2_pred) 
hist_list_categories(result, 'result/graph_step2.png')

# save result into osha_pred1.csv
osha_data['category_pred_step2'] = step2_pred

print('========================== step 3 ============================================')
# Combine with the result from tmproj_q1_step1
category_pred_step3 = []

for index, row in osha_data.iterrows():
    if row['category_pred_step2']:
        category_pred_step3.append(row['category_pred_step2'])
    else:
        if row['category_pred_step1']:
            category_pred_step3.append(row['category_pred_step1'])
        else:
            category_pred_step3.append('Others')
            
osha_data['category_pred_step3'] = category_pred_step3

print('========================== step 4 ============================================')
osha_data_other = osha_data[osha_data['category_pred_step3'] == 'Others']
osha_data_categorized = osha_data[osha_data['category_pred_step3'] != 'Others']

input_case = msia_title_case.append(osha_data_categorized['Title Case Aft'], ignore_index=True)
input_category = msia_category.append(osha_data_categorized['category_pred_step3'], ignore_index=True)

nb_clf3 = Pipeline([('vect', CountVectorizer(binary = True)), ('clf', MultinomialNB(fit_prior=False))])
nb_clf3.fit(input_case, input_category)
# manually check if the most informative terms make sense in step 3
show_most_informaitive_terms(nb_clf3.named_steps['vect'].get_feature_names(), nb_clf3.named_steps['clf'])

step4_pred = predict_with_threshold(nb_clf3, osha_data_other['Title Case Aft'], 0.3)

osha_data_other['category_pred_step4'] = step4_pred
osha_data_categorized['category_pred_step4'] = osha_data_categorized['category_pred_step3']
osha_data_pred2 = pd.concat([osha_data_other,osha_data_categorized])

hist_list_categories(osha_data_pred2['category_pred_step4'], 'result/graph_q1.png')
osha_data_pred2.to_csv('result/osha_q1.csv')
