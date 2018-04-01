# Semantic Similarity with Word2Vec

import gensim.models

words = ['amazing']  # to test word similarity
#words = ['prince','man','woman'] # to test word compositions
#words = ['MS_Dhoni','India','Ponting']

model_bin = 'c:/tools/GoogleNews-vectors-negative300.bin'  # set path
w2vmodel = gensim.models.KeyedVectors.load_word2vec_format(model_bin,binary=True)

try:
  if(len(words) == 3):
   print("---",words[0],'-',words[1],'+',words[2],"---")
   results = w2vmodel.most_similar(positive=[words[0],words[2]],negative=[words[1]])
  else:
   print("--- words similar to", words[0], "---")
   results = w2vmodel.most_similar(positive=[words[0]])
  
  for word,score in results:
       print(score,word)
except KeyError:
  print("Sorry that word doesn't exist!")
            
