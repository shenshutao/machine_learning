'''
The program trains data from Reuters Corpus using 2 classifiers:
    1. Support Vector Machine (SVM)
    2. Naive Bayes
for the categories 'money-fx' and 'interest'

Once the data is trained, the respective accuracy scores are displayed after
classifying the test data set

Usage: python reutersCorpus.py
'''

import sys
import math
import nltk
import random
from nltk.corpus import reuters
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression

#reload(sys)
#sys.setdefaultencoding('utf-8')


def get_word_features(category):
    """"Returns list of words that occur in all the documensts
    in specified category"""
    #print "Getting word features.."
    all_words = nltk.FreqDist(w.lower() for w in reuters.words(categories=category))
    word_features = list(all_words)[:5000]
    return word_features


def get_documents():
    """In each category ("earn", "cpu", etc.), the method takes all the file IDs
    (each category may have several IDs), and stores the list of words for the
    file ID, followed by the category label in one big list and returns that
    list"""
    #print "Getting documents.."
    documents = [
        (list(reuters.words(fileid)), category)
        for category in reuters.categories()  # E.g. "barley", "earn", "cpu" etc.
        for fileid in reuters.fileids(category)]  # E.g. test/14882, training/1077
    # shuffle documents for training and testing
    random.shuffle(documents)
    return documents


def document_features(document, word_features):
    """Returns features dictionary which contains data stating if each word in
    the word features is contained in the document words"""
    #print "Getting document features.."
    document_words = set(document)
    dw = list(document_words)
    features = {}
    # The reason that we compute the set of all words in a document, rather
    # than just checking if word in document, is that checking whether a word
    # occurs in a set is much faster than checking whether it occurs in a list
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    # print features.items()[1]
    return features


def categorise_data(category, featuresets):
    """Data from featuresets is labeled 1 if it belongs to positive category
    and appended to positive_data list; Otherwise it is labeled 0 and it is
    appended to negative data list. Positive and Negative data set is
    returned"""
    #print "Categorizing data.."
    positive_data = []
    negative_data = []
    for featureset in featuresets:
        data = featureset[0]
        data_cat = featureset[1]
        if data_cat == category:
            label = 1
            positive_data.append((data, label))
        else:
            label = 0
            negative_data.append((data, label))
    #print "POSITIVE DATA = %d" % len(positive_data)
    #print "NEGATIVE DATA = %d" % len(negative_data)
    return positive_data, negative_data


def split_data(positive_data, negative_data):
    """Train and Test data are built from positive and negative
    data and are returned"""
    #print "Splitting data.."
    train_data = []
    test_data = []
    split_factor = 0.7

    # Negative data size truncated and made equal to positive data size
    positive_data_size = len(positive_data)
    negative_data = negative_data[:positive_data_size]

    # Train data is formed by taking 70% of positive and 70% of negative data
    # Test data is formed by taking 30% of positive and 30% of negative data
    split_index = int(math.ceil(split_factor * positive_data_size))
    train_data = positive_data[:split_index] + negative_data[:split_index]
    test_data = positive_data[split_index:] + negative_data[split_index:]

    #print "SPLIT INDEX = %d" % split_index
    #print "TRAIN DATA = %d" % len(train_data)
    #print "TEST DATA = %d" % len(test_data)
    return train_data, test_data


def classify_words(category, word_features):
    """Classifiers are trained with Training data set and classify the test
    data set and print the accuracy score to the command line"""
    documents = get_documents()
    featuresets = [(document_features(d, word_features), c)
                   for (d, c) in documents]
    postive_data, negative_data = categorise_data(category, featuresets)
    train_set, test_set = split_data(postive_data, negative_data)

    classifier_svm = SklearnClassifier(LinearSVC()).train(train_set)
    classifier_nb = nltk.NaiveBayesClassifier.train(train_set)

    accuracy_svm = format((nltk.classify.accuracy(classifier_svm, test_set)))
    accuracy_nb = format(nltk.classify.accuracy(classifier_nb, test_set))
    print("SVM:",accuracy_svm, "NB:",accuracy_nb)

if __name__ == '__main__':

    category = sys.argv[1]
        
    #print "Category: %s" % category
    for i in range(0,5):    
        # Retrieves list of words occuring in that category
        word_features = get_word_features(category)
        classify_words(category, word_features)
