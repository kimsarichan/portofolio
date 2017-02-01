import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re

def readdata(file):
    data= pd.read_csv(os.path.join(os.path.dirname(__file__), file), header=0,delimiter="\t", quoting=3)
    return data

def clean_word(review):
    review_text = BeautifulSoup(review,"html.parser").get_text()
    review_text = re.sub("[^a-zA-Z]", " ", review_text)
    words = review_text.lower().split()
    stops = set(stopwords.words("english"))
    words = [w for w in words if not w in stops]
    return (words)

def clean_data(data):
    clean_data=[]
    for i in data["review"]:
        clean_data.append(" ".join(clean_word(i)))
    return clean_data
def bag_of_word():
    return
def main():
    data=readdata('labeledTrainData.tsv')
    train_data=data[:17500]
    test_data=data[17500:]
    #print train_data['review'][17499]
    print len(train_data)
    #print test_data['review'][17500]
    print len(test_data)
    #clean data test and train
    clean_data_train=clean_data(train_data)
    clean_data_test=clean_data(test_data)
    #transform data into feature vector
    vectorizer = CountVectorizer(analyzer="word", tokenizer=None, preprocessor=None,
                                 stop_words=None, max_features=5000)
    train_data_feature = vectorizer.fit_transform(clean_data_train)
    train_data_feature=train_data_feature.toarray()
    #random forest classifier
    forest = RandomForestClassifier(n_estimators=100)
    forest = forest.fit(train_data_feature,train_data["sentiment"])
    test_data_features = vectorizer.transform(clean_data_test)
    test_data_features = test_data_features.toarray()
    result=forest.predict(test_data_features)
    akurasi=0
    tidak_akurat=0
    j=0
    for i in range(17500,(len(test_data)+17500)):
        if test_data["sentiment"][i]==result[j]:
            akurasi+=1
        else:
            tidak_akurat+=1
        j+=1
    print (akurasi*1.0)/((akurasi+tidak_akurat)*1.0)



main()