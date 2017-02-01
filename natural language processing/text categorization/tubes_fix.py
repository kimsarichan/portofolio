import nltk
import re
import os
import nltk
from nltk.stem.porter import *
from nltk.stem.snowball import *
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
from sklearn.cluster import KMeans,AgglomerativeClustering,AffinityPropagation
from sklearn import metrics
import numpy
import collections
import random
import math
from sklearn.metrics.pairwise import cosine_similarity

def read_data(file):
    obj= open(file)
    hasil= obj.read()
    obj.close()
    return hasil

def read_class(path):
    file_training = os.listdir(path)
    training = []
    for i in file_training:
        j = path+"/"+ str(i)
        file = read_data(j)
        training.append(file)
    return training

def pre_processing_file(file):
    file=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', file)
    tokenizer = RegexpTokenizer(r'\w+')
    token=tokenizer.tokenize(file)
    post_tag=nltk.pos_tag(token)
    noun=[item[0] for item in post_tag if (item[1] == 'NN' or item[1] == 'NNP' or item[1] == 'NNPS' or item[1] == 'NNS' or item[1]=='FW')]
    stemmer = PorterStemmer()
    steam=[stemmer.stem(n) for n in noun]
    return steam

def cosine_similiarity(point,cluster):
    atas=0
    bawah_kiri=0
    bawah_kanan=0
    for i in range(len(cluster)):
        atas+=point[i]*cluster[i]
        bawah_kiri=point[i]**2
        bawah_kanan=point[i]**2
    return atas/(math.sqrt(bawah_kanan)*math.sqrt(bawah_kiri))

def nearest_cluster(point,cluster_p):
    d=0
    index=0
    for i in xrange(len(cluster_p)):
        distance=cosine_similiarity(point,cluster_p[i])
        print  "tes ",i,"distance",distance
        if (i==0):
            index=i
            d=distance
        elif (distance<=d):
            index =i
            d=distance
            print "hasil",d
    return index

def search_centroid(image):
    return numpy.mean(image,axis=0)

def createrandcentroid(tfidfmatrix,c):
    centroid=[]
    for i in c:
        centroid.append(tfidfmatrix[i])
    return centroid

def clustering(tfidfmatrix,cluster_p,label):
    c= random.sample(range(0,tfidfmatrix.shape[0]),cluster_p)
    centroid=createrandcentroid(tfidfmatrix,c)
    #print  centroid
    prev=[]
    j=0
    while(numpy.array_equal(centroid,prev)!=True):
        prev=centroid
        cluster={}
        j+=1
        print j
        cluster=collections.defaultdict(list)
        for i in range(len(tfidfmatrix)):
            cluster[nearest_cluster(tfidfmatrix[i],centroid)].append([tfidfmatrix[i],label[i],nearest_cluster(tfidfmatrix[i],centroid)])
            print tfidfmatrix[i],label[i],nearest_cluster(tfidfmatrix[i],centroid)
        centroid=[[] for i in range(cluster_p)]
        for i in cluster:
            centroid[i].append(search_centroid(cluster[i]))
    label_prediksi=[]
    label_real=[]
    for i in cluster:
            label_real.append(cluster[i][1])
            label_prediksi.append(cluster[i][2])
    return label_real,label_prediksi
category=["business","entertainment","politics","sport","tech"]
label=[]
preproc=[]

for i in range(len(category)):
    r_class=read_class('bbc/'+category[i])
    for j in r_class:
        hasil=pre_processing_file(j)
        preproc.append(" ".join(hasil))
        label.append(i)

vectorizer=TfidfVectorizer(min_df=3,stop_words='english')
tfidf_matrix =  vectorizer.fit_transform(preproc)
feature_names = vectorizer.get_feature_names()
label_real,label_prediksi=clustering(tfidf_matrix.toarray(),5,label)
# #kmeans
# km = KMeans(n_clusters=5,n_init=10, tol=1e-6)
# km.fit(tfidf_matrix)
# #hierarchical clustering
# hc = AgglomerativeClustering(n_clusters=957)
# hc.fit(tfidf_matrix.toarray())
# #affinity Propagation
#af = AffinityPropagation().fit(tfidf_matrix)

print "K Means"
print("Homogeneity: %0.3f" % metrics.homogeneity_score(label_real, label_prediksi))
print("Completeness: %0.3f" % metrics.completeness_score(label_real, label_prediksi))
print("V-measure: %0.3f" % metrics.v_measure_score(label_real, label_prediksi))
#
# print "Affinity Propagation"
# print("Homogeneity: %0.3f" % metrics.homogeneity_score(label, af.labels_))
# print("Completeness: %0.3f" % metrics.completeness_score(label,af.labels_))
# print("V-measure: %0.3f" % metrics.v_measure_score(label, af.labels_))
#
# print "Hierarchical Clustering"
# print("Homogeneity: %0.3f" % metrics.homogeneity_score(label, hc.labels_))
# print("Completeness: %0.3f" % metrics.completeness_score(label, hc.labels_))
# print("V-measure: %0.3f" % metrics.v_measure_score(label, hc.labels_))
# # print pre_processing_file(read_data('bbc/business/001.txt'))
