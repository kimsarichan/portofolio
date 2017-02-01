#import csv
import math

from collections import OrderedDict
def opendatafile(filename):
    f=open(filename)
    j=1
    m=[]
    for i in f:
        k=i.split()
        m.append(k)
    return m

def openitemfile(filename):
    f=open(filename)
    m=[]
    num=1
    for i in f:
        k=i.split('|')
        m.append(k)
        num+=1
    return m,num

a= sorted(opendatafile("data/u.data"),key=lambda ma:int(ma[1]))
item,len_item=openitemfile("data/u.item")
def data_movie(a,id):
    data=[]
    for i in range(len(a)):
        if int(a[i][1])>int(id) :
            break
        else:
            if int(a[i][1])== int(id):
                data.append(a[i][0])
    return data

def data_rating(a,id):
    data={}
    for i in range(len(a)):
        if int(a[i][1])>int(id) :
            break
        else:
            if int(a[i][1])== int(id):
                data[int(a[i][0])]=int(a[i][2])
    return data
#print(data_rating(a,'1'))

def intersect_dic(a,b):
    return {x:a[x] for x in a if x in b}

def dict_to_list(dict):
    data=[]
    for d in dict:
        data.append(dict[d])
    return data


def union(a,b):
    return list(set(a)&set(b))

def intersect(a,b):
    return list(set(a)| set(b))

def jaccard_coef(arraya,arrayb):
    return float(len(union(arraya,arrayb)))/float(len(intersect(arraya,arrayb)))

def find_jaccardall(len_item,data,id):
    data_jaccard={}
    movie=data_movie(data,id)
    for i in range(len_item):
        if (i != int(id)) :
            movieb=data_movie(data,i)
            data_jaccard[i]= jaccard_coef(movie,movieb)
    return data_jaccard

def search_name(item,id):
    return item[id-2][1]
def search_id(item,name):
    for i in item:
        if name in i[1]:
            return (int(i[0]))

def best_five(jacardall,item):
    sort_jc= sorted(jacardall,key=jacardall.__getitem__,reverse=True)
    for i in range(5):
        print i, ". " , search_name(item,sort_jc[i]),jacardall[sort_jc[i]]

#Corelation coefficient
def average(x):
    if(len(x)==0):
        return 0
    else:
        hasil=0.0
        for i in x :
            hasil += i

        return(hasil/len(x)*1.0)

def standard_deviasi(x):
    if(len(x)-1==0):
        return 0
    else:
        aver=average(x)
        hasil=0.0
        for i in x :
            j= i-aver
            hasil+=j**2
        return math.sqrt(hasil/float(len(x)-1))

def correlation(x,y):
    hasil_x=[]
    hasil_y =[]
    hasil=0.0
    for i in x:
        if standard_deviasi(x)==0:
            return 0
        else :
            hasil_x.append((i-average(x))/standard_deviasi(x))
    for i in y:
        if standard_deviasi(y)==0:
            return 0
        else :
            hasil_y.append((i-average(y))/standard_deviasi(y))
    if len(x)<31:
        return 0
    else :
        for i in range(len(x)):
            hasil+= hasil_y[i]*hasil_x[i]
        return hasil/(len(x)-1)

def find_corelation(len_item,data,id):
    data_corel={}
    for i in range(len_item):
        if (i != int(id)) :
            movie=data_rating(data,id)
            movieb=data_rating(data,i)
            #cari yang sama
            rating_a1= intersect_dic(movie,movieb)
            rating_b1= intersect_dic(movieb,movie)
            #sorting
            rating_a= OrderedDict(sorted(rating_a1.items(), key=lambda t: t[0]))
            rating_b=OrderedDict(sorted(rating_b1.items(), key=lambda t: t[0]))
            movie=dict_to_list(rating_a)
            movieb=dict_to_list(rating_b)
            #print search_name(item,i)
            data_corel[i]= correlation(movie,movieb)
            #print data_corel[i]
    return data_corel
#print standard_deviasi(data_rating(a,'1'))
print "Correlation Three Colors Red dan Three Colors Blue"
'''
j=(data_rating(a,59))
b=(data_rating(a,60))

rating_a= intersect_dic(j,b)
rating_b= intersect_dic(b,j)
#after sorting
rating_a= OrderedDict(sorted(rating_a.items(), key=lambda t: t[0]))
rating_b=OrderedDict(sorted(rating_b.items(), key=lambda t: t[0]))
#dict to list
rating_a_list=dict_to_list(rating_a)
rating_b_list=dict_to_list(rating_b)
print correlation(rating_a_list,rating_b_list)

print "Correlation Toy Story dan Golden Eye"
j=(data_rating(a,1))
b=(data_rating(a,2))

rating_a= intersect_dic(j,b)
rating_b= intersect_dic(b,j)
#after sorting
rating_a= OrderedDict(sorted(rating_a.items(), key=lambda t: t[0]))
rating_b=OrderedDict(sorted(rating_b.items(), key=lambda t: t[0]))
#dict to list
rating_a_list=dict_to_list(rating_a)
rating_b_list=dict_to_list(rating_b)
print correlation(rating_a_list,rating_b_list)

print "best five taxi driver"
id= search_id(item,"Taxi Driver")
corel= find_corelation(len_item,a,id)
best_five(corel,item)
print "best five toy story"
id= search_id(item,"Toy Story")
corel= find_corelation(len_item,a,id)
best_five(corel,item)
'''

#print(search_name(item,23))
print "golden eye and toy story"
print(jaccard_coef(data_movie(a,'1'),data_movie(a,'2')))
'''
#print(search_name(item,59))
#j= search_id(item,"Taxi Driver")
#jacardall= find_jaccardall(len_item,a,j)
#print("best five taxi driver")
#best_five(jacardall,item)
#print("best five Toy story")
#j= search_id(item,"Toy Story")
#jacardall= find_jaccardall(len_item,a,j)
#best_five(jacardall,item)
#sort_jc= sorted(jacardall,key=jacardall.__getitem__,reverse=True)
#print(sort_jc)
'''