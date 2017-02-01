import numpy as np
import matplotlib.pyplot as plt
import math
import  time

def generate_data(n):
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    class0=[]
    class1=[]
    data=[]
    for i in range(n):
        a=np.random.uniform(0,1,1)
        if a <=0.5:
            tmp1 = np.random.normal(0, math.sqrt(1))
            tmp2 = np.random.normal(2, math.sqrt(8))
            data1.append(tmp1)
            data2.append(tmp2)
            data.append([tmp1,tmp2,0])
            class0.append([tmp1,tmp2,0])
        else:
            tmp3 = np.random.normal(4, math.sqrt(10))
            tmp4 = np.random.normal(1, math.sqrt(3))
            data3.append(tmp3)
            data4.append(tmp4)
            data.append([tmp3,tmp4,1])
            class1.append([tmp3,tmp4,1])
    return  data1,data2,data3,data4,class0,class1,data

'''plot histogram'''
def plot_data(data1,data2,data3,data4,legend="Data Training"):
    plt.scatter(data1,data2,c='red',label="Class 0")
    plt.scatter(data3,data4,c='blue',label="Class 1")
    plt.title(legend)
    plt.show()

def histogram_data(data1,data2,data3,data4):
    plt. subplot (221)
    plt.title("data untuk x1")
    plt.hist(data1)
    plt. subplot (222)
    plt.title("data untuk x2")
    plt.hist(data2)
    plt. subplot (223)
    plt.title("data untuk x3")
    plt.hist(data3)
    plt. subplot (224)
    plt.title("data untuk x4")
    plt.hist(data4)
    plt.show()


'''KNN
1. Get knn
2. Define knn class
3. count missclacification in knn
4. Plot knn
'''
def eudi_2(train,test):
    hasil=((((test[0]-train[0])))*((test[0]-train[0])))+((((test[1]-train[1])))*((test[1]-train[1])))
    return math.sqrt(hasil)


def knn(train,test,k):
    neighbor=[]
    kn=[]
    for i in range(len(train)):
        x= eudi_2(train[i],test)
        neighbor.append([x,train[i][2]])
    neighbor = sorted(neighbor, key=lambda n: n[0])
    if(neighbor[0][0]==0.0):
        del neighbor[0]
    for i in range(k):
        kn.append(neighbor[i])
    return kn

def knn_class(knn):
    c0=0
    c1=0
    for i in range(len(knn)):
        if(knn[i][1]==0):
            c0+=1
        else :
            c1+=1
    if(c0>c1):
        return 0
    elif(c0<c1):
        return 1
    else:
        return "error"

def knn_all(train,test,k):
    error=0
    all=[]
    for i in range(len(test)):
        lis= knn(train,test[i],k)
        c=knn_class(lis)
        if(c !=test[i][2]):
            error+=1
        all.append([test[i][0],test[i][1],c])
    e= error*1.0/len(test)*1.0
    return all,e

def k_fold_validation(knn,s,data_training):
    hasil_error=[]
    k=len(data_training)/s
    a=[]
    for i in range(s):
        test = data_training[i*k:(i+1)*k]
        train = [_ for _ in data_training if _ not in test]
        all,e=knn_all(train,test,knn)
        hasil_error.append(e)
    return sum(hasil_error)/10*1.0
def k_fold_validationwithf1(knn,s,data_training):
    hasil_error=[]
    k=len(data_training)/s
    a=[]
    for i in range(s):
        test = data_training[i*k:(i+1)*k]
        train = [_ for _ in data_training if _ not in test]
        all,e=knn_all(train,test,knn)
        a.append(f1measure(test,all))
    return sum(a)/10*1.0


def f1measure(actual,predicted):
    tp=0
    fp=0
    fn=0
    tn=0
    for i in range(len(actual)):
        if(actual[i][2]==1 and predicted[i][2]==1):
            tp+=1
        elif(actual[i][2]==1 and predicted[i][2]==0):
            fn+=1
        elif(actual[i][2]==0 and predicted[i][2]==1):
            fp+=1
        elif(actual[i][2]==0 and predicted[i][2]==0):
            tn+=1
    precision= tp*1.0/(tp+fp)*1.0
    recall=tp*1.0/(tp+fn)*1.0
    f=2*((precision*recall)/(precision+recall)*1.0)
    return f

'''plot error'''
def plothasilerrornorm(k_coba, data_training,data_testing):
    hasil_error=[]
    for i in k_coba:
        all,e=knn_all(data_training,data_testing,i)
        hasil_error.append(e)
    if(data_testing==data_training):
        plt.plot([k for k in k_coba],[kn for kn in hasil_error], 'bo-',c='red',label='KNN training and training')
    else:
        plt.plot([k for k in k_coba],[kn for kn in hasil_error], 'bo-',c='green',label='KNN testing and training')

def plothasilerrorkfold(k_coba,data_training):
    hasil_error=[]
    for i in k_coba:
        hasil_error.append(k_fold_validation(i,10,data_training))
    plt.plot([k for k in k_coba],[kn for kn in hasil_error],'bo-',label='K Fold Cross Validation')

def plothasilerrorfmeasure(k_coba,data_training,data_testing):
    hasil_error=[]
    h=[]
    for i in k_coba:
        all,e=knn_all(data_training,data_testing,i)
        f=f1measure(data_testing,all)
        hasil_error.append(f)
    print hasil_error
    plt.plot([k for k in k_coba],[kn for kn in hasil_error],'bo-',c='black')

def plot_klasifikasi(knn,data_training,data_testing):
    all,e=knn_all(data_training,data_testing,knn)
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    for i in all:
        if i[2]==0:
            data1.append(i[0])
            data2.append(i[1])
        elif i[2]==1:
            data3.append(i[0])
            data4.append(i[1])
    plot_data(data1,data2,data3,data4,legend="Klasifikasi")

k_coba=[1,3,5,7,9,13,17,21,25,33,41,49,57]

''' data training'''
data1,data2,data3,data4,class0,class1,data_training=generate_data(500)
'''data testing'''
data1_testing,data2_testing,data3_testing,data4_testing,class0_testing,class1_testing,data_testing=generate_data(1000)
'''
#plot data
plothasilerrornorm(k_coba,data_training,data_testing)
plothasilerrornorm(k_coba,data_training,data_training)
plt.title("Hasil error missclasification KNN ")
plt.legend(loc="upper right")
plt.show()
plothasilerrorkfold(k_coba,data_training)
plt.title("Hasil 10-Fold cross validation")
plt.show()
'''
'''plot f1 measure'''
'''
plothasilerrorfmeasure(k_coba,data_training,data_testing)
plt.show()
'''
print k_fold_validationwithf1(13,10,data_training)
'''klasifikasi'''

plot_klasifikasi(7,data_training,data_testing)
plt.show()