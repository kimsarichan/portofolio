import re
import collections
import os
from decimal import *
def open_file(file):
    file_new = open(file, 'r')
    a=file_new.read()
    file_new.close()
    return a
def preprocessing_file(file):
    #1 Remove tag <p>
    review_text=re.sub(r'</?p[^>]*>', '', file)
    # 2. Remove non-letters
    letters_only = re.sub("[^a-zA-Z]", " ", review_text)
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()
    # 4. Remove Stopword
    sw = open("StopWords_Eng-Ind.txt", mode='r')
    stop = sw.readlines()
    sw.close()
    stop = [kata.strip() for kata in stop]
    stop = set(stop)
    meaningful_words = [w for w in words if not w in stop]
    return (" ".join(meaningful_words))

def bag_of_words(file, test='',train=''):
    if(test==''):
        bagsofwords = [collections.Counter(re.findall(r'\w+', f)) for f in file]
    else:
        bagsofwords = collections.Counter(re.findall(r'\w+', file))
        bow={}
        for i in bagsofwords:
            if i in train:
                bow[i]=bagsofwords[i]
        bagsofwords=bow
    return bagsofwords

def probability_array(train_kata,class_train):
    sum_kata = len(train_kata) + sum(class_train.values())
    probability = {}
    for i in train_kata:
        if i not in class_train:
            probability[i] = Decimal((1*1.0) / (sum_kata*1.0))
        else:
            probability[i] =  Decimal(((class_train[i]*1.0) + 1.0) / (sum_kata*1.0))
    return probability

def read_class(path):
    file_training = os.listdir(path)
    training = []
    for i in file_training:
        j = path+"/"+ str(i)
        file = preprocessing_file(open_file(j))
        training.append(file)
    bow = sum(bag_of_words(training), collections.Counter())
    return bow,len(file_training)

def hitung(test,probability_positif,probability_negatif,prior_positif,prior_negatif):
    positif=1
    negatif=1
    for i in test:
        tmp_positif=Decimal(probability_positif[i]**test[i])
        tmp_negatif=Decimal(probability_negatif[i]**test[i])
        positif=Decimal(positif*tmp_positif)
        negatif=Decimal(negatif*tmp_negatif)
    positif=Decimal(positif*prior_positif)
    negatif=Decimal(negatif*prior_negatif)
    if(positif>negatif):
        return "positif"
    elif(positif==negatif):
        return "neutral"
    else:
        return "negatif"

def test(path,kata,train_positif,train_negatif, prior_positif,prior_negatif,class_test=''):
    file_test = os.listdir(path)
    false = 0
    true = 0
    for i in file_test:
        test = preprocessing_file(open_file(path+'/' + i))
        bow_test = bag_of_words(test, test=True, train=kata)
        pos = hitung(bow_test, train_positif, train_negatif, prior_positif, prior_negatif)
        if pos != class_test:
            false += 1
        else:
            true += 1
    return false,true

def f1measure(false_negative,true_positive,false_positive,true_negative):
    precision=(true_positive*1.0)/((true_positive+false_positive)*1.0)
    recall=(true_positive*1.0)/((true_positive+false_negative)*1.0)
    f1=2*((precision*recall)/(precision+recall))
    return f1

def naive_bayes():
    #data training  negatif
    bow_negatif,jumlah_training_negatif=read_class('data training/neg')
    # data training positif
    bow_positif,jumlah_training_positif=read_class('data training/pos')
    #prior probability
    prior_positif=Decimal((jumlah_training_positif*1.0)/((jumlah_training_negatif+jumlah_training_positif)*1.0))
    prior_negatif=Decimal((jumlah_training_negatif*1.0)/((jumlah_training_negatif+jumlah_training_positif)*1.0))
    #data training all kata
    kata=bow_positif.copy()
    kata.update(bow_negatif)
    #probability positif
    probability_positif=probability_array(kata,bow_positif)
    #probability negatif
    probability_negatif=probability_array(kata, bow_negatif)
    #read_test
    false_negative,true_positive=test('data testing/pos',kata,probability_positif,probability_negatif, prior_positif,prior_negatif,class_test='positif')
    false_positive,true_negative=test('data testing/neg',kata,probability_positif,probability_negatif, prior_positif,prior_negatif,class_test='negatif')
    akurasi=(true_positive+true_negative)*1.0/(true_positive+false_negative+true_negative+false_positive)*1.0
    print "nilai akurasi :",(akurasi*100)
    print "nilai f1 measure :",(f1measure(false_negative,true_positive,false_positive,true_negative)*100)

naive_bayes()
#file=preprocessing_file(open_file("data training/neg/blog1.4.txt"))