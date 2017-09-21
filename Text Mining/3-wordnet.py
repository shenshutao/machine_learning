# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 00:19:41 2017
Workshop: IE - WordNet as lexical resource
@author: issfz
"""
from nltk.corpus import wordnet as wn

# To look up a word
wn.synsets('book')
# Look up with specified POS - NOUN, VERB, ADJ, ADV
wn.synsets('book', pos = wn.VERB)

# Let's examine a synset in more details: its definition, examples, lemma
ss = wn.synsets('book')[0]

print(ss.definition())
print(ss.examples())
ss.lemmas()
lem = ss.lemmas()[0]
lem.name()

# A synset has related synsets, for example, its hypernyms, hyponyms
ss = wn.synsets('vehicle')[0]
ss.hypernyms()
ss.hyponyms()

hyps = list(set([w for s in ss.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
