import csv
import numpy as np
def readdata(file):
    data = np.genfromtxt (file, delimiter=",")
    return data
data_training= readdata("training_set.csv")
data_testing=readdata("test_set.csv")

def prior(data,kelas):
    a=0
    for i in data:
        if (i[4]==float(kelas)):
            a+=1
    return a*1.0/len(data)*1.0

def likelihood(data, kelas, atribut,data_row):
    data_l=[]
    for i in data:
        if(i[4]==float(kelas)):
            data_l.append(i[atribut])
    x=np.array(data_l)
    sd=np.std(x)
    a= 1/(np.sqrt(2*np.pi*np.std(x)))
    mean=np.mean(x)
    c=(data_row[atribut]-mean)**2
    d= -(c)/(2*(sd)**2)
    b= np.exp(d)
    hasil=a*b
    return hasil

def posterior(data, kelas , row):
    ll=1
    for i in range(len(row)-1):
        ll*=likelihood(data,kelas,i,row)
    return ll*prior(data,kelas)

def map(data_training,data_testing):
    kelas=[]
    for i in data_testing :
        posterior0=posterior(data_training,0,i)
        posterior1=posterior(data_training,1,i)
        if(posterior0>posterior1):
            kelas.append(0)
        else:
            kelas.append(1)
    return kelas

map= map(data_training,data_testing)

def f1measure(actual,predicted):
    tp=0
    fp=0
    fn=0
    tn=0
    acc=0
    for i in range(len(actual)):
        if(actual[i][4]==1 and predicted[i]==1):
            acc+=1
            tp+=1
        elif(actual[i][4]==1 and predicted[i]==0):
            fn+=1
        elif(actual[i][4]==0 and predicted[i]==1):
            fp+=1
        elif(actual[i][4]==0 and predicted[i]==0):
            acc+=1
            tn+=1
    precision= tp*1.0/(tp+fp)*1.0
    recall=tp*1.0/(tp+fn)*1.0
    f=2*((precision*recall)/(precision+recall)*1.0)
    acc=acc*1.0/len(actual)*1.0
    return tp,fn,fp,tn,precision,recall,f,acc

tp,fn,fp,tn,precision,recall,f,acc=  f1measure(data_testing,map)
print "tp= ",tp
print "fn= ",fn
print "fp= ",fp
print "tn= ",tn
print "precission= ",precision
print "recall= ",recall
print "f1 measure= ",f
print "akurasi= ",acc
