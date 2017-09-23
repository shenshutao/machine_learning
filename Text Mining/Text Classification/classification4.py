# coding: utf-8
import pandas as pd
news=pd.read_table('r8-train-all-terms.txt',header=None,names = ["Class", "Text"])
news.head()

#Summarize the data by the news class
news.groupby('Class').describe()

#Select a subset from the dataframe. (crude money-fx trade)
subnews=news[(news.Class=="trade")| (news.Class=='crude')|(news.Class=='money-fx') ]
subnews.groupby('Class').describe()
print(subnews.shape)

#Count the length of each document
length=subnews['Text'].apply(len)
subnews=subnews.assign(Length=length)
subnews.head()

#Plot the distribution of the document length for each category
import matplotlib.pyplot as plt
subnews.hist(column='Length',by='Class',bins=50)

plt.show()
subnews.head()

#Define preprocessing function
import nltk
from nltk.corpus import stopwords
newstopwords=stopwords.words("English") + ['yuhao','the','is','it','may']
WNlemma = nltk.WordNetLemmatizer()

def pre_process(text):
    tokens = nltk.word_tokenize(text)
    tokens=[WNlemma.lemmatize(t) for t in tokens]
    tokens=[word for word in tokens if word not in newstopwords]
    text_after_process=" ".join(tokens)
    return(text_after_process)

#Apply the function on each document
subnews['Text'] = subnews['Text'].apply(pre_process)
subnews.head()

length=subnews['Text'].apply(len)
subnews=subnews.assign(Length=length)
subnews.head()

#split the data into training and testing
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(subnews.Text, subnews.Class, test_size=0.33, random_state=12)

#Create dtm by using word occurence
from sklearn.feature_extraction.text import CountVectorizer


count_vect = CountVectorizer( )

X_train_counts = count_vect.fit_transform(X_train)
X_train_counts.shape

count_vect.get_feature_names()


dtm1 = pd.DataFrame(X_train_counts.toarray().transpose(), index = count_vect.get_feature_names())
dtm1=dtm1.transpose()
dtm1.head()
dtm1.to_csv('dtm1.csv',sep=',')


# # Building a Naïve Bayes Model

#Create dtm by using Term Frequency. 
#Divide the number of occurrences of each word in a document 
#by the total number of words in the document: 
#these new features are called tf for Term Frequencies
#If set use_idf=True, which mean create dtm by using tf_idf

from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
X_train_tf.shape


#Building Modeling by using Naïve Bayes
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tf, y_train)


#Prediction on new documents
docs_new = ['Crude price is dropping ', 'rate is increasing']

X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tf_transformer.transform(X_new_counts)
#X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)
print(predicted)

#Build a pipeline: Combine multiple steps into one
from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer()),  
                     ('tfidf', TfidfTransformer()),
                      ('clf', MultinomialNB()),
                    ])


#Use pipeline to train the model
text_clf.fit(X_train,y_train ) 

#Test model accuracy
import numpy as np
from sklearn import metrics 
predicted = text_clf.predict(X_test)
#np.mean(predicted == y_test) 
print(metrics.confusion_matrix(y_test, predicted))
print(np.mean(predicted == y_test) )


# # Building a Decision Tree Model
#Decision Tree
from sklearn import tree
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                      ('clf', tree.DecisionTreeClassifier())
                    ])
text_clf.fit(X_train, y_train) 
predicted = text_clf.predict(X_test)

print(metrics.confusion_matrix(y_test, predicted))
print(np.mean(predicted == y_test) )


# # Building a SVM Model
#SVM
from sklearn.linear_model import SGDClassifier
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer(use_idf=True)),
                      ('clf', SGDClassifier(
                                            alpha=1e-3 
                                             ))
                    ])

text_clf.fit(X_train, y_train)  

predicted = text_clf.predict(X_test)
 
print(metrics.confusion_matrix(y_test, predicted))
print(np.mean(predicted == y_test) )
#y_test.value_counts()

print(metrics.classification_report(y_test, predicted))


import itertools
import matplotlib.pyplot as plt
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
cnf_matrix = confusion_matrix(y_test, predicted)
plot_confusion_matrix(cnf_matrix, classes=['crude','money_fx','trade'],
                      title='Confusion matrix, without normalization')
plt.figure()
plt.show()


# # Introduce the GridSearch Method
from sklearn.model_selection import GridSearchCV
parameters = {
                  'tfidf__use_idf': (True, False),
                   'clf__alpha': (1e-2, 1e-3),
                }

#text_clf = Pipeline([('vect', CountVectorizer()),
#                    ('tfidf', TfidfTransformer(use_idf=True)),
#                      ('clf', SGDClassifier(
#                                            alpha=1e-3 
#                                             ))
#                    ])


# If we give this parameter a value of -1, 
#grid search will detect how many cores are installed and uses them all:

gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
gs_clf = gs_clf.fit(X_train, y_train)
for param_name in sorted(parameters.keys()):
    print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))


