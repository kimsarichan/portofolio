import numpy as np
import math
import matplotlib.pyplot as plt

def readdata(file):
    a= [line.strip().split(',') for line in open(file)]
    for i in a :
        i[0]=float(i[0])
        i[1]=float(i[1])
        i[2]=float(i[2])
        i[3]=float(i[3])
        i[4]=int(i[4])
    return a


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def turunan_sigmoid(x):
    return x*(1-x)

def maju_hidden(data,hide,weight_input,weight_output):
    i_data=[]
    for i in range(hide):
        i_data.append(sigmoid(np.sum([weight_input[i][j] * data[j] for j in range(len(data))])))
    i_output = sigmoid(np.sum([weight_output[j] * i_data[j] for j in range(len(i_data))]))
    return i_data,i_output

def backward_hidden(predict,input,data,actual,weight_input,weight_output,lr,hide):
    out_error = actual-predict
    in_error = []
    for i in range(hide):
        in_error.append(weight_output[i]*out_error)
    for i in range(len(weight_input)):
        for j in range(len(weight_input[i])):
            weight_input[i][j] += lr * data[j] * turunan_sigmoid(input[i]) * in_error[i]
    for i in range(len(weight_output)):
        weight_output += lr * input[i] * turunan_sigmoid(predict) * out_error
    return weight_input,weight_output
#inisialisasi
weight_input = np.random.uniform(0,1,(4,4))
weight_output = np.random.uniform(0,1,(4,1))

#data normal
data= readdata('occupancy_normal.csv')
validasi= readdata('validasi.csv')
testing= readdata('testing.csv')

'''
#data biasa
data= readdata('occupancy.csv')
validasi= readdata('validasi_biasa.csv')
testing= readdata('testing_biasa.csv')
'''
hidden=4
lr=0.009
input=[i[:4] for i in data]
output = [i[4] for i in data]
output_validasi=[i[4] for i in validasi]
validasi=[i[:4] for i in validasi]
output_testing=[i[4] for i in testing]
testing=[i[:4] for i in testing]
mse_list=[]
mse_list_valid=[]
mse_list_testing=[]
#mse training training
for i in range(100):
    mse=0
    for i in range(len(input)):
        i_data,i_output = maju_hidden(input[i],hidden,weight_input,weight_output)
        mse+=(float(output[i])-i_output)**2
        weight_input,weight_output = backward_hidden(i_output,i_data,
                                    input[i],float(output[i]),weight_input,weight_output,lr,4)
    mse_list.append(mse/len(input)*1.0)
#mse training validasi
    mse=0
    for i in range(len(validasi)):
        i_data,i_output = maju_hidden(validasi[i],hidden,weight_input,weight_output)
        mse+=(float(output_validasi[i])-i_output)**2
    mse_list_valid.append(mse/len(input)*1.0)
    k=0
#mse training testing
    mse=0
    for i in range(len(testing)):
        i_data,i_output = maju_hidden(testing[i],hidden,weight_input,weight_output)
        mse+=(float(output_testing[i])-i_output)**2
    mse_list_testing.append(mse/len(input)*1.0)
'''akurasi'''
k=0
for i in range(len(testing)):
        i_data,i_output = maju_hidden(testing[i],hidden,weight_input,weight_output)
        if(round(i_output)==output_testing[i]):
            print testing[i]
            k+=1
            print "actual: ",output_testing[i],"hasil prediksi: ",i_output
print "hasil akurasi:" ,float(k)/float(len(testing))

plt.plot([i for i in range(100)],mse_list)
plt.plot([i for i in range(100)],mse_list_valid)
plt.plot([i for i in range(100)],mse_list_testing)
plt.show()
