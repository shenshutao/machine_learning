# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 00:19:41 2017
Workshop: IE - Using Stanford taggers
@author: issfz
"""

import nltk
from nltk import word_tokenize

sent = '''Professor Tan Eng Chye, NUS Deputy President and Provost, and Professor 
Menahem Ben-Sasson, President of HUJ signed the joint degree agreement at NUS, 
in the presence of Ambassador of Israel to Singapore Her Excellency Amira Arnon 
and about 30 invited guests, on July 03, 2013.
'''
doc = '''The National University of Singapore and The Hebrew University of Jerusalem (HUJ) are launching a Joint Doctor of Philosophy (PhD) degree programme in biomedical science from August 2013.

Professor Tan Eng Chye, NUS Deputy President (Academic Affairs) and Provost, and Professor Menahem Ben-Sasson, President of HUJ signed the joint degree agreement at NUS, in the presence of Ambassador of Israel to Singapore Her Excellency Amira Arnon and about 30 invited guests.

The new joint PhD programme is a collaboration between the Yong Loo Lin School of Medicine and the Faculty of Science at NUS with the HUJ Faculties of Medicine and Science. Students enrolled in the programme will divide their time between both campuses in Singapore and Jerusalem, Israel, spending a minimum of nine months at each institution. Two NUS students have already been selected for the inaugural intake and they will begin their programme in the new academic year starting this August.

NUS President Professor Tan Chorh Chuan said, “We are excited to further deepen our ties with HUJ through this new joint PhD programme. HUJ is highly respected internationally for its outstanding scientific research and its application. As the programme leverages on the complementary academic strengths of our two institutions, I am confident that it will offer a unique and world-class learning experience for our students and an excellent platform for our faculty to drive for even higher levels of excellence. This partnership also opens up more opportunities for researchers and students from both our universities to break new ground in biomedical science.”

Prof Menahem Ben-Sasson, President of the Hebrew University of Jerusalem, said, “We are proud of our relationship with NUS, which is one of the leading academic research institutions in Asia, and a model for its huge investment in research, teaching and globalisation. Through Singapore’s CREATE programme, we already have two student exchange programmes with NUS and a joint research venture. This new joint PhD programme is yet another step in strengthening our ties at all academic levels. The joint programme will enable students from each university to spend at least nine months in the other university, and to be exposed to their host country’s scientific advances and cultural experiences - a major asset in today’s interconnected global scientific community.” 

The joint PhD programme by NUS and HUJ will help to train a core group of biomedical scientists who will have international research experience with a solid footing in Asia. The strong tradition of research and educational excellence at NUS and HUJ allows both institutions to complement each other in the scientific frontier and the collaboration will offer its students the best in academic training and ample opportunities for exposure to different cultures.  

The joint PhD programme aims to take in between two to three students from each institution each year for the next four years. Each institution will conduct its own selection, in accordance with respective standard requirements for acceptance into a PhD programme. Student will pay tuition fees set by their home institution for the entire duration of the programme. NUS-registered students can also apply for the NUS Research Scholarship. 

NUS and HUJ have previously collaborated in establishing the NUS-HUJ Cellular and Molecular Mechanisms of Inflammation Research Programme in 2010, which is a part of the CREATE (Campus for Research Excellence And Technological Enterprise) programme of Singapore’s National Research Foundation.
'''

# ===== Tagging using Stanford Software =====
''' Installation Instruction
1. Download stanford-postagger-full-2017-06-09.zip and stanford-ner-2017-06-09.zip 
   from https://nlp.stanford.edu/software/
2. Unzip the two zip files into your destination folder, e.g. "C:/tools/"
'''

# Import StanfordPOSTagger and StanfordNERTagger from nltk.tag.stanford
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger

# Set JAVAHOME variable to the directory containin Java on your computer
import os
java_path = '/usr/bin/java'
os.environ['JAVAHOME'] = java_path

# Using Stanford POS Tagger
# set the path for POS tagger: the jar file and the model
pos_model_path = '/Users/shutao/Desktop/Text Mining/Workshops/week3/stanford-postagger-full-2017-06-09/models/english-bidirectional-distsim.tagger'
pos_jar_path = '/Users/shutao/Desktop/Text Mining/Workshops/week3/stanford-postagger-full-2017-06-09/stanford-postagger.jar'

# Initialize the tagger
st_pos=StanfordPOSTagger(pos_model_path, pos_jar_path)
st_pos.tag(word_tokenize(sent))


# Using Stanford NER Tagger
# set the path for NER tagger: the jar file and the model
ner_model_path = '/Users/shutao/Desktop/Text Mining/Workshops/week3/stanford-ner-2017-06-09/classifiers/english.all.3class.distsim.crf.ser.gz'
ner_jar_path = '/Users/shutao/Desktop/Text Mining/Workshops/week3/stanford-ner-2017-06-09/stanford-ner.jar'

st_ner = StanfordNERTagger(ner_model_path, ner_jar_path)
sent_ne = st_ner.tag(word_tokenize(sent))
sent_ne

# Check out the 7 class tagged english.muc.7class.distsim.crf.ser.gz model for more flexibility.
# It tags Currency, Location, Percentages along with Persons, Organizations etc.
ner7_model_path = '/Users/shutao/Desktop/Text Mining/Workshops/week3/stanford-ner-2017-06-09/classifiers/english.muc.7class.distsim.crf.ser.gz'
st_ner7 = StanfordNERTagger(ner7_model_path, ner_jar_path)
sent_ne7 = st_ner7.tag(word_tokenize(sent))
sent_ne7

# To get the entities from the tagged result
from itertools import groupby

for tag, chunk in groupby(sent_ne7, lambda x:x[1]):
    if tag != "O":
        print("%-12s"%tag, " ".join(w for w, t in chunk))
        
# Any problems of the above approach of calling Stanford tools?

# ===== Using Standford CoreNLP =====
'''
# 1. Download stanford-corenlp-full-2017-06-09.zip 
#   from https://stanfordnlp.github.io/CoreNLP/
# 2. Unzip to your target folder, eg. C:/tools/
# 3. Install a 3rd party python wrapper, such as stanfordcorenlp
#    with prompt line command "pip install stanfordcorenlp"
#    (Reference: https://github.com/Lynten/stanford-corenlp    )
# 4. Go to the CoreNLP installation folder
#    Start CoreNLP server first at the windows commandline:
#    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000    
# 5. Open web browser, go to http://localhost:9000
     Test CoreNLP on the web UI first.
'''

from stanfordcorenlp import StanfordCoreNLP

# Method 1: Create StanfordCoreNLP object
nlp = StanfordCoreNLP('/Users/shutao/Desktop/Text Mining/Workshops/week3/stanford-corenlp-full-2017-06-09/')

# Method 2: Using an existing server
# The CoreNLP server must have been started earlier
nlp2 = StanfordCoreNLP('http://localhost', port=9000)

# Simple usage
print('Tokenize:', nlp.word_tokenize(sent))
print('Part of Speech:', nlp.pos_tag(sent))
print('Named Entities:', nlp.ner(sent))
print('Constituency Parsing:', nlp.parse(sent))
print('Dependency Parsing:', nlp.dependency_parse(sent))

# General API call. The output format can be selected.
props={'annotators': 'tokenize,ssplit,pos,ner','pipelineLanguage':'en','outputFormat':'json'}
output = nlp.annotate(sent, properties=props)

# The output than can be examined as an json object
import json
outputj = json.loads(output)
outputj.keys()
se = outputj['sentences'][0]
se.keys()
se['tokens']
