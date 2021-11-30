import pandas as pd
import matplotlib.pyplot as plt
import os
import regex

import nltk
#nltk.download('stopwords')
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer, PorterStemmer

import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, plot_confusion_matrix

from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import conlltags2tree, tree2conlltags
from matplotlib import pyplot as plt
import re
import time
from collections import Counter

import nltk
from nltk.stem import PorterStemmer

from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import conlltags2tree, tree2conlltags
from matplotlib import pyplot as plt
import re
import time
from collections import Counter
os.chdir(r'C:\Users\KADAVADK\Desktop\MSIS 5193\Project')
################################################
#================Tutorial Data==================#
# Using  Description Column for sentiment analysis #
#################################################

#url = 'https://github.com/RobertSCookOSU/MSIS5193_BGJRGroup_Project/blob/main/Final%20Data/final_dataset_comparison_description.csv'
#df = pd.read_csv(url, index_col=0)
desc_data = pd.read_csv('final_dataset_comparison_description.csv')
desc_data.columns
#print(desc_data)
#desc_data.rename(columns={'text': 'Description'}, inplace=True)

desc_data['Description']=desc_data['Description'].fillna("NaN")
#==========================================
# Adjust the case of the text so that all
# values are lowercase
#==========================================

desc_data['Description'] = desc_data['Description'].apply(lambda x: " ".join(x.lower() for x in x.split()))

desc_data['Description'][2]
desc_data['Description'][5]

#=========================================
# Remove the numerical values as well as
# punctuation from the text.
#=========================================
patterndigits = '\\b[0-9]+\\b'
desc_data['Description'] = desc_data['Description'].str.replace(patterndigits,'')

patternpunc = '[^\w\s]'
desc_data['Description'] = desc_data['Description'].str.replace(patternpunc,'')

desc_data['Description'][2]
desc_data['Description'][5]

#=====================================
# Remove stop words from the data by
# using the dataset stop_words found
# in the nltk library
#=====================================
stop = stopwords.words('english')

# Before removal of stopwords
#desc_data['Description'][2]
#desc_data['Description'][5]

desc_data['Description'] = desc_data['Description'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

# After removal of stopwords
desc_data['Description'][2]
desc_data['Description'][5]

#=========================================
# Remove the  names from the data
#=========================================
remove_names = ["oklahoma","city",",","auction.com",".","zip","code","approximately"]

desc_data['Description'] = desc_data['Description'].apply(lambda x: " ".join(x for x in x.split() if x not in remove_names))

desc_data['Description'][2]
desc_data['Description'][5]

#======================================
# Stem the data using PorterStemmer()
#======================================
porstem = PorterStemmer()

desc_data['Description'] = desc_data['Description'].apply(lambda x: " ".join([porstem.stem(word) for word in x.split()]))

desc_data['Description'][2]
desc_data['Description'][5]
###################################################################################
#####Function NER#############
#####################################################################
def desc_data_ner(chunker):
    treestruct = ne_chunk(pos_tag(word_tokenize(chunker)))
    entitynn = []
    entityjj = []
    entityg_air = []
    entityvb = []
    for y in str(treestruct).split('\n'):
        if 'GPE' in y or 'GSP' in y:
            entityg_air.append(y)
        elif '/VB' in y:
            entityvb.append(y)
        elif '/NN' in y :
            entitynn.append(y)
        elif '/JJ' in y:
            entityjj.append(y)
    stringnn = ''.join(entitynn)
    stringjj = ''.join(entityjj)
    stringvb = ''.join(entityvb)
    stringg = ''.join(entityg_air)
    return stringnn, stringjj, stringvb, stringg
#####################################################################################################
#Logic NER
#####################################################################################################
desc_data['NN'] = ''
desc_data['VB'] = ''
desc_data['JJ'] = ''
desc_data['GEO'] = ''
i = 0
for x in desc_data['Description']:
    entitycontainer = desc_data_ner(x)
    desc_data.at[i,'NN'] = entitycontainer[0]
    desc_data.at[i,'JJ'] = entitycontainer[1]
    desc_data.at[i,'VB'] = entitycontainer[2]
    desc_data.at[i,'GEO'] = entitycontainer[3]
    i += 1
#It takes time to process the code hence commented
#desc_data['NN'].unique().tolist()
#desc_data['JJ'].unique().tolist()
#desc_data['VB'].unique().tolist()
#desc_data['GEO'].unique().tolist()
#===============================
#frequency plot
#==============================
#Noun
fdistribution = nltk.FreqDist(desc_data['NN'])
fdistribution.plot(10,title= 'Frequency distribution of  frequently occuring Nouns')
#AdJ
fdistribution = nltk.FreqDist(desc_data['JJ'])
fdistribution.plot(10,title= 'Frequency distribution of  frequently occuring Adjective')

#Verb
fdistribution = nltk.FreqDist(desc_data['VB'])
fdistribution.plot(10,title= 'Frequency distribution of  frequently occuring Verb')

#Geo or location
fdistribution = nltk.FreqDist(desc_data['GEO'])
fdistribution.plot(10,title= 'Frequency distribution of  frequently occuring location')
#################################################################################################
#================================
# Create a document-term matrix
#================================
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()

tokens_data = pd.DataFrame(vectorizer.fit_transform(desc_data['Description']).toarray(), columns=vectorizer.get_feature_names())

tokens_data.columns



# display all column names
#print(tokens_data.columns.tolist())


# Retrieve the top 10 in terms of volume
sort_text = tokens_data.sum()

sort_text.sort_values(ascending = False).head(10)

#============================================
# Perform Latent Dirichlet Allocation (LDA)
#============================================
vectorizer = CountVectorizer(max_df=0.8, min_df=4, stop_words='english')

doc_term_matrix = vectorizer.fit_transform(desc_data['Description'].values.astype('U'))

doc_term_matrix.shape


# Generate the LDA with 5 topics to divide
# the text into; set the seed to 35 so that
# we end up with the same result
LDA = LatentDirichletAllocation(n_components=5, random_state=35)
LDA.fit(doc_term_matrix)

# Retrieve words in the first topic 
first_topic = LDA.components_[0]

# Sort the indexes according to probability 
# values using argsort()
top_topic_words = first_topic.argsort()[-10:]

# Output the words to the console screen
for i in top_topic_words:
    print(vectorizer.get_feature_names()[i])

# Print the 10 words with highest 
# probabilities for all five topics
for i,topic in enumerate(LDA.components_):
    print(f'Top 10 words for topic #{i}:')
    print([vectorizer.get_feature_names()[i] for i in topic.argsort()[-10:]])
    print('\n')

# Add a column in the dataset with the topic number
topic_values = LDA.transform(doc_term_matrix)
topic_values.shape
desc_data['topic'] = topic_values.argmax(axis=1)

desc_data.head()

#==================================================
# Perform Non-Negative Matrix Factorization (NMF)
#==================================================
tfidf_vect = TfidfVectorizer(max_df=0.8, min_df=5, stop_words='english')

doc_term_matrix2 = tfidf_vect.fit_transform(desc_data['Description'].values.astype('U'))


nmf = NMF(n_components=5, random_state=42)

nmf.fit(doc_term_matrix2)

first_topic = nmf.components_[0]
top_topic_words = first_topic.argsort()[-10:]

for i in top_topic_words:
    print(tfidf_vect.get_feature_names()[i])

# Top 10 words for each topic
for i,topic in enumerate(nmf.components_):
    print(f'Top 10 words for topic #{i}:')
    print([tfidf_vect.get_feature_names()[i] for i in topic.argsort()[-10:]])
    print('\n')

# Add a column with the topic values. 
topic_values2 = nmf.transform(doc_term_matrix2)
desc_data['topic2'] = topic_values2.argmax(axis=1)
desc_data.head()

#################################################
#=======Sentiment Analysis Classification=======#
# Perform an analysis based on the sentiment    #
# contained within the dataset          #
#################################################

#============================================================================
# Create a term-frequency inverse-document-frequency (TF-IDF)
# matrix with sklearn:
# TF  = (Frequency of a word in the document)/(Total words in the document)
# IDF = Log((Total number of docs)/(Number of docs containing the word))
#============================================================================
features = desc_data['Description']
#print(features)
# Use only the 2500 most frequently occurring terms
# Use only those terms that occur in a maximum of 80% of the documents
# but at least in 7 documents

vectorizer = TfidfVectorizer (max_features=2500, min_df=7, max_df=0.8, stop_words=stop)

processed_features = vectorizer.fit_transform(features).toarray()
print(processed_features)
#==========================================
# Generate a training and testing dataset
#==========================================
labels = desc_data['Description']

# Test dataset will be 20%
# Results in a training set of 80%
X_train, X_test, y_train, y_test = train_test_split(processed_features, labels, test_size=0.2, random_state=0)

# Train a machine learning model, randomforest, using
# the training dataset
text_classifier = RandomForestClassifier(n_estimators=200, random_state=0)
text_classifier.fit(X_train, y_train)

# Time to test the model using the predict() function
predictions = text_classifier.predict(X_test)
print(predictions)

#===================================
# Evaluate the newly trained model
#===================================
cm = confusion_matrix(y_test,predictions)
print(cm)

#plot_confusion_matrix(text_classifier, X_test, y_test)


print(classification_report(y_test,predictions))

print(accuracy_score(y_test, predictions))

#########################################################################################
#Train a machine learning model, Naive bayes using
# the training dataset
###########################################################################################
text_classifier = GaussianNB(priors=None)

text_classifier.fit(X_train, y_train)

# Time to test the model using the predict() function
predictions = text_classifier.predict(X_test)
print(predictions)

#===================================
# Evaluate the newly trained model
#===================================
cm = confusion_matrix(y_test,predictions)
#print(cm)

plot_confusion_matrix(text_classifier, X_test, y_test)


print(classification_report(y_test,predictions))

print(accuracy_score(y_test, predictions))