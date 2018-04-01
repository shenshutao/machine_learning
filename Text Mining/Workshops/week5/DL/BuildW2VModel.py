#!/usr/bin/env python

'''
Program loads data from the given path, parses the text data and uses it to
create a Word2Vec Model. Word2Vec Model is saved to the disk persistently.
'''

# Usage:
# python TrainW2VModel.py {path_to_data}
# python TrainW2VModel.py ./Data


import sys
import os
import re

import nltk
from nltk.corpus import stopwords

import gensim.models
from bs4 import BeautifulSoup

import warnings


STOP_WORDS = set(stopwords.words("english"))


def get_file_contents(fname):
    """
    Returns contents from input file
    """
    with open(fname) as f:
        rows = f.readlines()
    return rows


def remove_html(review):
    """
    The following ignores the following bs4 warning:
    UserWarning: "." looks like a filename, not markup.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", lineno=182)
        return BeautifulSoup(review, "html.parser").get_text()

def review_to_wordlist(review, remove_stopwords=True):
    """
    Function removes HTML, Non-letters and optionally Stopwords and converts
    words to lower case and splits them into a list of words. The list of words
    is returned
    """

    # 1. Remove HTML
    #review_text = remove_html(review)
    review_text = review
    
    # 2. Remove non-letters
    review_text = re.sub("[^a-zA-Z]", " ", review_text)

    # 3. Convert words to lower case and split them
    words = str(review_text.lower()).split()

    # 4. Remove stopwords
    if remove_stopwords:
        words = [w for w in words if w not in STOP_WORDS]
    return words


def review_to_sentences(review, tokenizer, remove_stopwords=True):
    """
    Define a function to split a review into parsed sentences, where
    each sentence is a list of words. Fucntion returns the parsed data
    """
    # 1. Use the NLTK tokenizer to split the paragraph into sentences
    raw_sentences = tokenizer.tokenize(review.strip())

    # 2. Loop over each sentence
    sentences = []
    for sentence in raw_sentences:
        if len(sentence) > 0:
            words = review_to_wordlist(sentence, remove_stopwords)
        sentences.append(words)

    # Return the list of sentences (each sentence is a list of words,
    # so this returns a list of lists
    return sentences


def get_parsed_data(raw_data):
    """Function parses raw data and return the parsed data"""
    # Load the punkt tokenizer
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    data = []
    for raw_d in raw_data:
        data += review_to_sentences(raw_d, tokenizer)
    return data


def load_data(fpath):
    """Function loads data present in the given file path and
    stores the data after parsing it"""
    print("Loading data...")
    data = []
    if os.path.isdir(fpath):
        dir_list = os.listdir(fpath)
        for directory in dir_list:
            new_path = fpath + '/' + directory
            file_list = os.listdir(new_path)
            for f in file_list:
                file_path = new_path + '/' + f
                raw_data = get_file_contents(file_path)
                parsed_data = get_parsed_data(raw_data)
                data += parsed_data
    return data


def train_model(train_data):
    """Function trains and creates Word2vec Model using parsed
    data and returns trained model"""
    model = gensim.models.Word2Vec(train_data, min_count=2)
    return model


def get_w2v_model(data):
    """Function creates trained model and saved model persistently to disk"""
    model_name = "word2vec_model"
    trained_model = train_model(data)
    trained_model.save(model_name)
    print("Saved %s model successfully" % model_name)


if __name__ == '__main__':

    fpath = sys.argv[1]
    data = load_data(fpath)

    # for d in data[:10]:
    #    print d

    w2v_model = get_w2v_model(data)
