# Deep Learning Workshop
#     - Raja @I2R

* Pre-requisites: 
     - Python 2.7 (Easy to just install Anaconda IDE and use Spyder)
	 - Main Modules: NLTK (packages reqd: reuters,punkt,stopwords), Gensim, Scipy
	 - Other modules: Pls see import in .py codes
	 
* Functionality Test:
    
  I.
  
    $ python  RunBaseline.py money-fx
	
	Expected Output: Accuracy scores for SVM and NB (5 runs) . Runtime: 5-6 mins
	
  II. 
  
    $ python BuildW2VModel.py ./Data
	
	Expected Output : The file 'word2vec_model' (size about 17.3MB) gets created . Runtime: 1 or 2 mins
	
  III

    $ python RunW2V.py ./Data word2vec_model money-fx
	
	Expected Output : Accuracy scores of W2V model (5 runs) . Runtime : 15-20 mins
	
	 
	 