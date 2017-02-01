import numpy
import csv
from itertools import product
from collections import defaultdict
input={0: [[-0.3439,-0.1459,0.1479,0.3376],[0.1355,0.3434,0.6452,0.8393],[0.6532,0.8432,1.139,1.337]],
        1: [[-0.315,-0.315,0.1398,0.3002],[0.1343,0.3196,0.5877,0.7674],[0.5991,0.7767,1.035,1.215]],
        2: [[-0.3465,-0.1485,0.1473,0.3195],[0.141,0.3453,0.6436,0.8336],[0.6883,0.8415,1.139,1.337]]}
outpufunc=[0.03673,0.5608,3.644,0.1635,0.5495,4.603,22.57,0.6209,1.041,-0.582,-0.05544,3.716,-0.3042,-0.3326,3.546,12.12,-3892,2.724,7.706,-1.211,14.32,6.15,0.004888,3.707,16.56,22.13,13.4]
input2={0:[[0.0,0.0,0.15,0.36],[0.15,0.36,0.5,0.8],[0.5,0.8,1,1]],
        1:[[0,0,0.18,0.3],[0.18,0.3,0.55,0.6],[0.55,0.6,1,1]],
        2:[[0,0,0.1,0.4],[0.1,0.4,0.55,0.81],[0.55,0.81,1,1]]}

rule={0:{0:{0:0,1:2,2:3},1:{0:0,1:2,2:3},2:{0:0,1:0,2:3}},
      1:{0:{0:0,1:2,2:3},1:{0:0,1:2,2:3},2:{0:1,1:2,2:3}},
      2:{0:{0:0,1:2,2:3},1:{0:0,1:2,2:3},2:{0:0,1:2,2:3}}
      }

def readdata(file):
    a= [line.strip().split(',') for line in open(file)]
    for i in a :
        i[0]=float(i[0])
        i[1]=float(i[1])
        i[2]=float(i[2])
        i[3]=int(i[3])
    return a

def tampfunction(inputraw,inmf):
    if (inputraw>inmf[2] and inputraw<=inmf[3]):
        return -(-inputraw-inmf[3])/(inmf[3]-inmf[2])
    elif (inputraw>inmf[0] and inputraw<inmf[1]):
        return (inputraw-inmf[0])/(inmf[1]-inmf[0])
    elif(inputraw>= inmf[1] and inputraw<=inmf[2]):
        return 1
    else:
        return 0

def inputfunc(membership,data):
    input_gen=[]
    for i in membership:
        input_gen.append(tampfunction(data,i))
    return input_gen

def fk(data):
    data_hasil=[]
    for i in range(len(data)-1):
        d= inputfunc(input2[i],data[i])
        data_hasil.append(d)
    return data_hasil

def fuzzyrule(data,rule):
    loop=list(product([0,1,2],repeat = 3))
    hasil_all=defaultdict(list)
    for i in loop:
        hasil = rule[i[0]][i[1]][i[2]]
        d=[]
        if(i[0]<len(data[0])):
            d.append(data[0][i[0]])
        if(i[1]<len(data[1])):
            d.append(data[1][i[1]])
        if(i[2]<len(data[2])):
            d.append(data[2][i[2]])
        if d==[]:
            continue
        else:
            hasil_nilai =min(d)
        hasil_all[hasil].append(hasil_nilai)
    max0= max(hasil_all[0])
    max1= max(hasil_all[1])
    max2= max(hasil_all[2])
    max3= max(hasil_all[3])
    #print max0,max1,max2,max3
    return max0,max1,max2,max3

def sugeno(max0,max1,max2,max3):
    hasil = ((max0*0)+(max1*1)+(max2*2)+(max3*3))/(max0+max1+max2+max3)
    return round(hasil)

def fuzzy(data,rule):
    hasil_fuzzy=[]
    for i in data:
        data_member= fk(i)
        max0,max1,max2,max3=fuzzyrule(data_member,rule)
        hasil = sugeno(max0,max1,max2,max3)
        hasil_fuzzy.append(hasil)
    return hasil_fuzzy

def akurasi(data_asli,data_train):
    akurasi=0
    for i in range(len(data_asli)):
        print "actual: ",data_asli[i][3],"predict: ",data_train[i]
        if (data_asli[i][3]==int(data_train[i])):
            akurasi+=1
    print "data benar :",akurasi
    print "data salah :",len(data_asli)-akurasi
    print "akurasi :", (akurasi*1.0)/len(data_asli)*1.0
    return (akurasi*1.0)/len(data_asli)*1.0


data= readdata('Dataset UNS_fix.csv')
hasil =fuzzy(data,rule)
akurasi(data,hasil)
