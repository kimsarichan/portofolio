import pandas as pd
import os
import math
import csv
import matplotlib.pyplot as plt
import numpy as np
import random
#knowledge based
def similiarity(item_a_feature,item_b_feature,weight):
    if (type(item_a_feature) and type(item_b_feature) !='list' ):
        if(item_a_feature==item_b_feature):common_a_b=1
        else:common_a_b=0
        if(common_a_b!=0):
            total=weight*common_a_b
            return total
        else:
            return 0
    else:
        common_a_b=list(set(item_a_feature)&(item_b_feature))
        common_a_b=len(common_a_b)
        if(len(item_a_feature)>len(item_b_feature)):max=len(item_a_feature)
        else:max=len(item_b_feature)
        if(max!=0):
            return (((common_a_b*1.0)/(max*1.0))*weight)

def sim(item_a,item_b):
    total=0
    w=0
    weight=1/((len(item_a)-1)*1.0)
    for i in item_a:
        if(i=='id'):continue
        else:
            total=total+similiarity(item_a[i],item_b[i],weight)
            w=w+weight
    return ((total*1.0)/(w*1.0))


def recon_vector(reference_sim,recon,rate):
    if rate==1:
        rate=0.3
    elif rate==2:
        rate = 0.6
    elif rate==3:
        rate=1
    recon=recon+(reference_sim*rate)
    return recon


def recon_nonclass(data_user,data_item,recon):
    for i in data_user:
        if i == 'tags':
            continue
        if i=='id':
            continue
        if data_user['edu_fieldofstudies']==data_item['discipline_id']:
            recon = recon + 1
            continue
        if i=='experience':
            if data_item['career_level']==1 and (data_user['experience']==1 or data_user['experience']==2)  :
                recon = recon + 1
            elif data_item['career_level']==2 and (data_user['experience']==1 or data_user['experience']==2)  :
                recon = recon + 1
            elif data_item['career_level']==3 and data_user['experience']>=2  :
                recon = recon + 1
            elif data_item['career_level']==4 and data_user['experience']>=5  :
                recon = recon + 1
            elif data_item['career_level']==5 and data_user['experience']>=6  :
                recon = recon + 1
            elif data_item['career_level']==6 and data_user['experience']>=7  :
                recon = recon + 1
            continue
        if i=='career_level':
            if data_user['career_level']==1:
                if(data_item['employment']!=1):
                    recon=recon+1

        if i!='edu_fieldofstudies':
            if i == 'edu_degree':
                if data_item['career_level'] == 2 and (data_user[i] == 1 or data_user[i] == 2):
                    recon = recon + 1
                elif data_item['career_level'] > 2 and (data_user[i] == 1 or data_user[i] == 2 or data_user[i] == 2):
                    recon = recon + 1
            else:
                if data_user[i]==data_item[i]:
                    if i=='region':
                        if data_user['country']==data_item['country']:
                            recon=recon+1
                    else:
                        recon = recon + 1
    return recon

def inference_user_with_top_n(user,data_user,data_item,item,item_test,n,data_test,data_train,file,tmp):
    f_cf = open(file + 'cf.csv', 'wb')
    cf_file = csv.writer(f_cf)
    cf_file.writerow(('user', 'item', 'hasil cf', 'real'))
    f_kbs = open(file + 'kbs.csv', 'wb')
    kbs_file = csv.writer(f_kbs)
    kbs_file.writerow(('user', 'item', 'hasil kbs', 'real'))
    tmp = open(tmp + ".csv", 'wb')
    tmp_file = csv.writer(tmp)
    tmp_file.writerow(('user', 'item', 'hasil kbs', 'hasil cf'))
    jumlah = 0
    jumlah_kbs = 0
    jumlah_cf = 0
    user_preference = {}
    for i in data_test:
        item_recon = {}
        user_preference[i] = []
        average_rating_user = sum(d[1] for d in data_train[i]) / len(data_train[i])
        for j in item_test:
            for k in data_train[i]:
                if k[0] == j:
                    continue
            jumlah_operasi = 0
            item_recon[j] = 0
            similiarity_list = []
            for train in data_train[i]:
                similiarity = sim(data_item[j], data_item[train[0]])
                similiarity_list.append([similiarity, train[1]])
            similiarity_list.sort(key=lambda x: x[0], reverse=True)
            if (len(similiarity_list) >= 20):
                similiarity_list = similiarity_list[:20]
            for similiarity in similiarity_list:
                item_recon[j] = recon_vector(similiarity[0], item_recon[j], similiarity[1])
                jumlah_operasi = jumlah_operasi + 1
            item_recon[j] = item_recon[j] + recon_nonclass(data_user[i], data_item[j], item_recon[j])
            cf = predicteditem(data_train, i, item, j, average_rating_user)
            tmp_file.writerow((i, j, (((item_recon[j] * 1.0) / (jumlah_operasi * 1.0)) * 3.0), cf))
            user_preference[i].append([j, cf, (((item_recon[j] * 1.0) / (jumlah_operasi * 1.0)) * 3.0)])

        jumlah += len(data_test[i])
        print jumlah

        a = sorted(user_preference[i], key=lambda x: x[2], reverse=True)
        user_choice_kbs = a[:n]
        b = sorted(user_preference[i], key=lambda x: x[1], reverse=True)
        user_choice_cf = b[:n]

        for k in user_choice_kbs:
            for j in data_test[i]:
                if j[0] == k[0]:
                    print "berhasil"
                    jumlah_kbs += 1
                    kbs_file.writerow((i, j[0], k[2], j[1]))

        for k in user_choice_cf:
            for j in data_test[i]:
                if j[0] == k[0]:
                    print "berhasil cf"
                    jumlah_cf += 1
                    cf_file.writerow((i, j[0], k[2], j[1]))



def inference_user(data_user,data_item,item,file,data_test,data_train):
    f=open(file,'wb')
    writer = csv.writer(f)
    writer.writerow(('user', 'item', 'hasil cf','cf_norm','hasil kbs','max_kbs','real'))
    jumlah=0
    #print data_test
    for i in data_test:
        item_recon={}
        average_rating_user = sum(d[1] for d in data_train[i]) / len(data_train[i])
        for j in data_test[i] :
            jumlah_operasi=0
            item_recon[j[0]]=0
            similiarity_list=[]
            for train in data_train[i]:
                similiarity=sim(data_item[j[0]],data_item[train[0]])
                similiarity_list.append([similiarity,train[1]])
            similiarity_list.sort(key=lambda x:x[0],reverse=True)
            if (len(similiarity_list) >= 20):
                similiarity_list = similiarity_list[:20]
            for similiarity in similiarity_list:
                item_recon[j[0]] = recon_vector(similiarity[0], item_recon[j[0]], similiarity[1])
                jumlah_operasi = jumlah_operasi + 1
            item_recon[j[0]]=item_recon[j[0]]+recon_nonclass(data_user[i],data_item[j[0]],item_recon[j[0]])
            cf=predicteditem(data_train,i,item,j[0],average_rating_user)
            jumlah_operasi=jumlah_operasi+(len(data_user[i])-1)
            writer.writerow((i,j[0],(cf*3.0),cf,item_recon[j[0]],jumlah_operasi,j[1]))
        jumlah=jumlah+1
        print jumlah
    f.close()

#collaborative filtering
def getrating(user,user1,item):
    for i in user[user1]:
        if i[0]==item:
            return i[1]
    return None

def similiarity_cf(user,user1,user2):
    atas=0
    kiri=0
    kanan=0
    average_rating_user1 = sum(d[1] for d in user[user1])*1.0 / len(user[user1])*1.0
    average_rating_user2 = sum(d[1] for d in user[user2])*1.0 / len(user[user2])*1.0
    for i in user[user1]:
            if getrating(user,user2,i[0])!=None:
                atas += (getrating(user,user2, i[0]) - average_rating_user2) * (getrating(user,user1, i[0]) - average_rating_user1)
                kiri += (getrating(user,user2, i[0]) - average_rating_user2) ** 2
                kanan += (getrating(user,user1, i[0]) - average_rating_user1) ** 2
    bawah=(math.sqrt(kiri)*math.sqrt(kanan)*1.0)
    if(bawah==0):
        return 0
    else:
        return (atas*1.0)/(bawah*1.0)

def predicteditem(user,user_test,item,item_tujuan,average_rating_user):
    atas=0
    bawah=0
    similiarity_list=[]
    if item_tujuan in item:
        try:
            for i in item[item_tujuan]:
                average_rating_user = sum(d[1] for d in user[i[0]]) / len(user[i[0]])
                similiarity_list.append([similiarity_cf(user,user_test, i[0]),getrating(user,i[0],item_tujuan),average_rating_user])
            if  similiarity_list!=[]:
                similiarity_list.sort(key=lambda x:x[1],reverse=True)
                if(len(similiarity_list)>=20):
                    similiarity_list = similiarity_list[:20]
                for i in similiarity_list:
                    atas += i[0]* (i[1]-i[2])
                    bawah += abs (i[0])
        except:
            return average_rating_user
    if bawah==0:
        return average_rating_user
    else:
        return average_rating_user + (atas*1.0/bawah*1.0)

#hybrid recommendation
def hybrid(hasil_kbs,hasil_cf,influence):
    return ((hasil_kbs*(1-influence))+(hasil_cf*influence))*3.0

def hybrid_recomendation(file,influence_1,influence_2,hasil):
    hybrid_file=open(hasil,'wb')
    test = pd.read_csv(os.path.join(os.path.dirname(__file__), file), delimiter=",", quoting=6)
    writer = csv.writer(hybrid_file)
    writer.writerow(('user', 'item','hasil moderate', 'hasil liberal'))
    max_kbs=(max(test['hasil kbs'])*1.0)
    max_cf=(max(test['hasil cf'])*1.0)
    for i in range(len(test['user'])):
        kbs=(test['hasil kbs'][i]*1.0)/max_kbs
        cf= (test['hasil cf'][i]*1.0)/max_cf
        hasil_hybrid_1=hybrid(kbs,cf,influence_1)
        hasil_hybrid_2 = hybrid(kbs, cf, influence_2)
        writer.writerow((test['user'][i],test['item'][i],hasil_hybrid_1,hasil_hybrid_2))
    hybrid_file.close()

def preprocessing(user, item, interaksi):
    data_user= pd.read_csv(os.path.join(os.path.dirname(__file__),user),delimiter="\t", quoting=13)
    data_item= pd.read_csv(os.path.join(os.path.dirname(__file__), item),delimiter="\t", quoting=13)
    data_ekstrak=pd.read_csv(os.path.join(os.path.dirname(__file__), interaksi),delimiter="\t", quoting=3)
    item={}
    user={}
    print len(data_ekstrak['item'])
    for i in range(len(data_ekstrak['item'])):
        if data_ekstrak['interaction'][i] == 4:
            interaction = 0
        elif data_ekstrak['interaction'][i] == 3:
            interaction = 3
        elif data_ekstrak['interaction'][i] == 2:
            interaction = 2
        elif data_ekstrak['interaction'][i] == 1:
            interaction = 1
        if((data_ekstrak['item'][i] not in item) and (data_ekstrak['item'][i] in data_item['id']) and (data_ekstrak['user'][i] in data_user['id'])):
            item[data_ekstrak['item'][i]] = []
            item[data_ekstrak['item'][i]].append([data_ekstrak['user'][i],interaction ])
        elif((data_ekstrak['item'][i] in item) and (data_ekstrak['item'][i] in data_item['id']) and (data_ekstrak['user'][i] in data_user['id'])):
            item[data_ekstrak['item'][i]].append([data_ekstrak['user'][i],interaction])
        if((data_ekstrak['user'][i] not in user) and (data_ekstrak['user'][i] in data_user['id']) and (data_ekstrak['item'][i] in data_item['id'])):
            user[data_ekstrak['user'][i]] = []
            user[data_ekstrak['user'][i]].append([data_ekstrak['item'][i],interaction])
        elif((data_ekstrak['user'][i] in user) and (data_ekstrak['user'][i] in data_user['id']) and (data_ekstrak['item'][i] in data_item['id']) ):
            user[data_ekstrak['user'][i]].append([data_ekstrak['item'][i],interaction])
    data_ekstrak=[]
    data_item_new={}
    for i in range(len(data_item['title'])):
            dict_item = {}
            dict_item['career_level']=data_item['career_level'][i]
            dict_item['discipline_id']=data_item['discipline_id'][i]
            dict_item['industry_id']=data_item['industry_id'][i]
            dict_item['country']=data_item['country'][i]
            dict_item['region']=data_item['region'][i]
            dict_item['employment'] = data_item['employment'][i]
            dict_item['tags']=str(data_item['tags'][i]).split(',')
            data_item_new[data_item['id'][i]]=dict_item
    data_item = []
    data_user_new={}
    for i in range(len(data_user['id'])):
            dict_user={}
            dict_user['career_level'] = data_user['career_level'][i]
            dict_user['discipline_id']=data_user['discipline_id'][i]
            dict_user['country']=data_user['country'][i]
            dict_user['region']=data_user['region'][i]
            dict_user['industry_id'] = data_user['industry_id'][i]
            dict_user['edu_fieldofstudies'] = data_user['edu_fieldofstudies'][i]
            dict_user['experience']= data_user['experience_years_experience'][i]
            dict_user['edu_degree'] = data_user['edu_degree'][i]
            data_user_new[data_user['id'][i]]=dict_user
    return user,item,data_user_new,data_item_new

def test_cfandkbs(file):
    # # test cf kbs
    test = pd.read_csv(os.path.join(os.path.dirname(__file__), file ), delimiter=",", quoting=6)

    cf = 0
    kbs = 0
    mse_cf=0
    mse_kbs=0
    jumlah=len(test['real'])
    for i in range(len(test['real'])):
        # print test['real'][i],test['hasil cf'][i]
        cf=(test['hasil cf'][i]/6.0)*3.0
        mse_cf += ((round(cf) - round(test['real'][i])) ** 2)
        mse_kbs += ( round(((test['hasil kbs'][i] * 1.0) / (test['max_kbs'][i] * 1.0)) * 3.0) - round(test['real'][i])) ** 2
    print "RMSE CF",math.sqrt(mse_cf/(jumlah*1.0))
    print "RMSE KBS",math.sqrt(mse_kbs/(jumlah*1.0))
    return math.sqrt(mse_cf/(jumlah*1.0)),math.sqrt(mse_kbs/(jumlah*1.0))

def testhybrid(file):
    #test hybrid
    test = pd.read_csv(os.path.join(os.path.dirname(__file__), file), delimiter=",", quoting=7)
    mse_liberal = 0
    mse_moderate= 0
    jumlah = len(test['real'])
    for i in range(len(test['real'])):
        print (round(test['hasil moderate'][i]) )
        print test['real'][i]
        print int(test['real'][i])
        mse_moderate += ((round(test['hasil moderate'][i]) - int(test['real'][i])) ** 2)
        mse_liberal += ((round(float(test['hasil liberal'][i])) - int(test['real'][i])) ** 2)

    print "RMSE liberal",math.sqrt(mse_liberal/(jumlah*1.0))
    print "RMSE moderate",math.sqrt(mse_moderate/(jumlah*1.0))
    return math.sqrt(mse_liberal/(jumlah*1.0)),math.sqrt(mse_moderate/(jumlah*1.0))

def hasil_running(user,file):
    test = pd.read_csv(os.path.join(os.path.dirname(__file__), file), delimiter=",", quoting=7)
    rekomendasi=True
    for i in range(len(test['real'])):
        if test['user'][i]==user:
            if (test['hasil kbs'][i] != 'None'):
                print "item yang direkomendasikan kbs"
                print test['item'][i]
                print "nilai prediksi",test['kbs'][i]
                rekomendasi=True
            elif (test['hasil cf'][i] != 'None'):
                print "item yang direkomendasikan collaborative filtering "
                print test['item'][i]
                print "nilai prediksi",test['hasil cf'][i]
                rekomendasi=True
            elif (test['liberal'][i] != 'None'):
                print "item yang direkomendasikan hybrid liberal"
                print test['item'][i]
                print "nilai prediksi", test['liberal'][i]
                rekomendasi=True
            elif (test['moderate'][i] != 'None'):
                print "item yang direkomendasikan hybrid moderate"
                print test['item'][i]
                print "nilai prediksi", test['moderate'][i]
                rekomendasi=True
    if rekomendasi==False:
        print "tidak ada item yang direkomendasikan"

def grafik_rmse():
    hasil_cf=[]
    hasil_kbs=[]
    hasil_liberal=[]
    hasil_moderate=[]
    for i in range(10):
        RMSE_CF, RMSE_KBS=test_cfandkbs('hasil_kfold_'+str(i)+'.csv')
        hasil_cf.append(RMSE_CF)
        hasil_kbs.append(RMSE_KBS)
        hybrid_recomendation('hasil_kfold_'+str(i)+'.csv',0.25,0.5,'hasil_kfold_hybrid_'+str(i)+'.csv')
        RMSE_LIBERAL,RMSE_MODERATE=testhybrid('hasil_kfold_hybrid_'+str(i)+'.csv')
        hasil_liberal.append(RMSE_LIBERAL)
        hasil_moderate.append(RMSE_MODERATE)
    metode = ('cf', 'kbs', 'moderate', 'liberal')
    y_pos = np.arange(len(metode))
    performance = (sum(hasil_cf)/float(len(hasil_cf)),sum(hasil_kbs)/float(len(hasil_kbs)), sum(hasil_moderate)/float(len(hasil_moderate)), sum(hasil_liberal)/float(len(hasil_liberal)))
    # average performance = (sum(hasil_cf)/float(len(hasil_cf)),sum(hasil_kbs)/float(len(hasil_kbs)), sum(hasil_moderate)/float(len(hasil_moderate)), sum(hasil_liberal)/float(len(hasil_liberal)))
    plt.barh(y_pos, performance, align='center',color='0.75')
    plt.yticks(y_pos, metode)
    plt.title('Hasil nilai rata rata rmse')
    plt.show()
    return (sum(hasil_cf)/float(len(hasil_cf)),sum(hasil_kbs)/float(len(hasil_kbs)), sum(hasil_moderate)/float(len(hasil_moderate)), sum(hasil_liberal)/float(len(hasil_liberal)))

#main program
if __name__ == "__main__":

    user, item, data_user_new, data_item_new=preprocessing('users.csv','items.csv','extracted_20.csv')
    # user_test={}
    # user_train={}
    # k_fold=10
    # item_train={}
    # item_test={}
    # len_interaksi=0
    # n=10
    # hasil=0
    # for k in [25]:
    #         jumlah_training=0
    #         jumlah=0
    #         jumlah_train=0
    #         for i in user:
    #             user_test[i] = random.sample(user[i],int(round(len(user[i])*0.4)))
    #             jumlah+=len(user_test[i])
    #             user_train[i] = [j for j in user[i] if j not in user_test[i]]
    #             jumlah_train+=len(user_train[i])
    #             for j in user_train[i]:
    #                 if j[0] in item_train:
    #                     item_train[j[0]].append([i, j[1]])
    #                 else:
    #                     item_train[j[0]] = []
    #                     item_train[j[0]].append([i, j[1]])
    #             for j in user_test[i]:
    #                     if j[0] in item_test:
    #                         item_test[j[0]].append([i, j[1]])
    #                     else:
    #                         item_test[j[0]] = []
    #                         item_test[j[0]].append([i, j[1]])
    #         f = open('data test_15_new.csv', 'wb')
    #         writer = csv.writer(f)
    #         writer.writerow(('user', 'item', 'real'))
    #         for i in user_test:
    #             for j in user_test[i]:
    #                 writer.writerow((i, j[0], j[1]))
    #         f.close()
    #         inference_user_with_top_n(user,data_user_new,data_item_new,item,item_test,n,user_test,user_train,"hasil_15item_15user.csv","hasil_allprediction_15item_15user.csv")
    #hybrid_recomendation('hasil_allprediction_15item_15user.csv.csv', 0.75, 0.5, 'hasil_hybrid_15_new.csv')