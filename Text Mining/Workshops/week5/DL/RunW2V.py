#!/usr/bin/env python

'''
Program takes the following as inputs when being executed (in the stated order):
1. Path to data
2. Word2Vector Model
3. Categories to perform text classification on

Flow of Execution:
- Word2Vector Averages for each document chosen is computed
- Word2Vec Average is tagged with label 1 if it represents a positive document
- Word2Vec Average is tagged with label 0 if it represents a negative document
- Positive and Negative data sets are constructed
- 70:30 split is done on the positive and negative data sets to create
  Train and Test Data sets
- SVM is used to train on the Train set and classifies the Test set
- Accuracy score is displayed to command line after SVM classifies the Test set

'''

# Usage:
# python <script> {path_to_data} {model} {category}
# python TrainTestW2V.py ./Data w2v_model earn


import sys
import os
import math
import random

from nltk.corpus import reuters

import gensim.models

import BuildW2VModel

from sklearn.svm import LinearSVC
# from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression


reuters_category = set(reuters.categories())


def select_elements(seq, perc):
    """Select a defined percentage of the elements of seq."""
    return seq[::int(100.0/perc)]


def percentage_completion(count, dir_list):
    """Displays the percent completed while iterating through a list"""
    #print count/len(dir_list)*100, " % complete...         \r",


def print_data(data):
    """Prints category and number of vectors in each category"""
    for k, v in data.items():
        print(k, len(v))



def merge_neg_vectors(neg):
    """Merges all Negative Vector Averages from various categories"""
    neg_data = {}
    for pos_cat, data_list in neg.items():
        print(pos_cat)
        vector_list = []
        for data in data_list:
            for vectors in data.values():
                vector_list += vectors
        neg_data[pos_cat] = vector_list
    return neg_data


def split_vector_label(data_set):
    """Splits (Vector, Label) tuples into separate lists"""
    random.shuffle(data_set)
    vectors = []
    labels = []
    for data in data_set:
        vec = data[0]
        label = data[1]
        vectors.append(vec)
        labels.append(label)
    return vectors, labels


def check_set_size(pos, neg):
    """Checks sizes of positive and negative data sets and makes
    them equal if they are different"""
    random.shuffle(pos)
    random.shuffle(neg)
    #print "Pos: %d   Neg: %d" % (len(pos), len(neg))
    if len(neg) > len(pos):
        limit = len(pos)
        neg = neg[:limit]
        #print "Final Sizes    Pos: %d   Neg: %d" % (len(pos), len(neg))
    return pos, neg


def get_vector_average(vectors):
    """Computes the vector average from a list of vectors"""
    vector_list_size = len(vectors)
    vector_sum = vectors[0]
    for vector in vectors[1:]:
        # print vector
        vector_sum += vector
    vector_avg = vector_sum / vector_list_size
    # print vector_avg
    # print vector_sum
    return vector_avg


def get_doc2vec(fname, trained_model):
    """Generates a vector average for each document using the trained model"""
    raw_data = BuildW2VModel.get_file_contents(fname)
    word_list = BuildW2VModel.get_parsed_data(raw_data)
    w2vmodel = gensim.models.Word2Vec.load(trained_model)
    doc_vectors = []
    for words in word_list:
        for word in words:
            try:
             vector = w2vmodel[word]
            except KeyError:
             continue
            doc_vectors.append(vector)
    return get_vector_average(doc_vectors)


def get_doc_vectors(dir_list, cat_path, w2v_model, isPos=True):
    """Craetes (vector, label) tuples for data in a given category"""
    vectors = []
    count = 0.0
    for doc in dir_list:
        fpath = cat_path + '/' + doc
        vec = get_doc2vec(fpath, w2v_model)
        if isPos:
            vec_label = (vec, 1)
        else:
            vec_label = (vec, 0)
        vectors.append(vec_label)
        percentage_completion(count, dir_list)
        count += 1
    return vectors


def get_positive_vectors(data_path, w2v_model, categories):
    """Generates Positive Vector Averages for all documents in given category"""
    #print "Generating Positive Vector Averages"
    data = {}
    for category in categories:
        cat_path = data_path + '/' + category
        dir_list = os.listdir(cat_path)
        vectors = get_doc_vectors(dir_list, cat_path, w2v_model, isPos=True)
        data[category] = vectors
    return data


def get_negative_vectors(data_path, w2v_model, categories):
    """Generates Negative Vector Averages for all documents except
       documents from specified category"""
    #print "Generating Negative Vector Averages"
    data = {}
    for category in categories:
        dir_list = os.listdir(data_path)
        cat_path = data_path + '/' + category
        cat_file_list = os.listdir(cat_path)

        neg_set_size = len(cat_file_list) # number of files needed for neg data set
        # print "Negative Set Size = %d" % neg_set_size
        neg_category = list(set(dir_list) - set([category])) # all cat excpet 1 cat
        neg_category = list(set(neg_category).intersection(reuters_category))

        data[category] = []
        neg_files = []
        count = 0.0
        for cat in neg_category:
            cat_path = data_path + '/' + cat
            cat_file_list = os.listdir(cat_path)
            new_list = []
            for fname in cat_file_list:
                new_fname = cat + '/' + fname
                new_list.append(new_fname)
            neg_files += new_list
        random.shuffle(neg_files)
        neg_files = neg_files[:neg_set_size]
        vectors = get_doc_vectors(neg_files, data_path, w2v_model, isPos=False)
        data[category] = vectors
    return data


def gen_train_test_sets(pos, neg):
    """Generates Train and Test Sets by taking 70-30 split from
       positive and negative data"""
    data = {}
    #print "Generating Train and Test Sets..."
    for category, vec in pos.items():
        pos_vec, neg_vec = check_set_size(vec, neg[category])
        split_index = int(math.ceil(0.7 * len(pos_vec)))
        train = pos_vec[:split_index] + neg_vec[:split_index]
        test = pos_vec[split_index:] + neg_vec[split_index:]
        # splits data to vectors and corresponding labels
        X_train, y_train = split_vector_label(train)
        X_test, y_test = split_vector_label(test)

        train_set = {'X_train': X_train, 'y_train': y_train}
        test_set = {'X_test': X_test, 'y_test': y_test}
        data[category] = [train_set, test_set]
    return data


def load_data(data_path, w2v_model, categories):
    """Method loads the positive and negative data sets and constructs the
    train and test sets from them; Train and Test data sets are returned in
    a dictionary format"""
    # Method gives (vector average, label) for each document in the pos category
    # {cat1: [(vec1, 1), (vec2, 1), (vec3, 1), ...],
    #  cat2: [(vec1, 1), (vec2, 1), (vec3, 1),...]}
    data_pos = get_positive_vectors(data_path, w2v_model, categories)

    #print "\nPositive Data Summary:"
    #print_data(data_pos)

    # Method merges all the negative vectors for the pos category
    # {pos_cat1: [(vec1, 0), (vec2, 0), (vec3, 0), ...],
    #  pos_cat2: [(vec1, 0), (vec2, 0), (vec3, 0),...]}
    data_neg = get_negative_vectors(data_path, w2v_model, categories)

    #print "\nNegative Data Summary:"
    #print_data(data_neg)


    # Method generates train and test sets for each cateogry to be tested
    # {cat1: [
    #           X_train: [vec1, vec2, vec3, ...],
    #           y_train: [label1, label2, label3, ...],
    #           X_test:  [vec1, vec2, vec3, ...],
    #           y_test: [label1, label2, label3, ...]
    #        ]
    #  cat2: [
    #           X_train: [vec1, vec2, vec3, ...],
    #           y_train: [label1, label2, label3, ...],
    #           X_test:  [vec1, vec2, vec3, ...],
    #           y_test: [label1, label2, label3, ...]
    #        ]
    # }
    data_sets = gen_train_test_sets(data_pos, data_neg)
    return data_sets


def train_and_test(data):
    """Trains and Tests Data using Losgistic Regression Model"""
    for cat, sets in data.items():
        X_train, y_train = sets[0]['X_train'], sets[0]['y_train']
        X_test, y_test = sets[1]['X_test'], sets[1]['y_test']

        classifier = LogisticRegression()
        classifier.fit(X_train, y_train)
        accuracy = classifier.score(X_test, y_test)
        #print "Category: %s" % cat
        #print "Classifier: Logistic Regression"
        print("W2V Accuracy: %f" % accuracy)

        
if __name__ == '__main__':

    data_path = sys.argv[1]
    w2v_model = sys.argv[2]
    categories = sys.argv[3:]

    for i in range(0,5):
     data_sets = load_data(data_path, w2v_model, categories)

     # Method trains and tests data and prints accuracy to command line
     #print "Data Report:"
     #print
     train_and_test(data_sets)
