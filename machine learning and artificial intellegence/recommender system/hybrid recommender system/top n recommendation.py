import os
import pandas as pd
import csv
def prediksi_user_cf_kbs(data):
    user_cf={}
    user_kbs={}
    for i in range(len(data['user'])):
        if data['user'][i] not in user_cf:
            user_cf[data['user'][i]]=[]
            user_cf[data['user'][i]].append([data['user'][i],data['item'][i],data['hasil cf'][i]])
            user_kbs[data['user'][i]] = []
            user_kbs[data['user'][i]].append([data['user'][i], data['item'][i], data['hasil kbs'][i]])
        else:
            user_cf[data['user'][i]].append([data['user'][i], data['item'][i], data['hasil cf'][i]])
            user_kbs[data['user'][i]].append([data['user'][i], data['item'][i], data['hasil kbs'][i]])
    return user_cf,user_kbs
def data_test_user(data):
    user={}
    for i in range(len(data['user'])):
        if data['user'][i] not in user:
            user[data['user'][i]] = []
            user[data['user'][i]].append([data['user'][i], data['item'][i], data['real'][i]])
        else:
            user[data['user'][i]].append([data['user'][i], data['item'][i], data['real'][i]])
    return user

def prediksi_liberal_moderate(data):
    user_liberal = {}
    user_moderate = {}
    for i in range(len(data['user'])):
        if data['user'][i] not in user_liberal:
            user_liberal[data['user'][i]] = []
            user_liberal[data['user'][i]].append([data['user'][i], data['item'][i], data['hasil liberal'][i]])
            user_moderate[data['user'][i]] = []
            user_moderate[data['user'][i]].append([data['user'][i], data['item'][i], data['hasil moderate'][i]])
        else:
            user_liberal[data['user'][i]].append([data['user'][i], data['item'][i], data['hasil liberal'][i]])
            user_moderate[data['user'][i]].append([data['user'][i], data['item'][i], data['hasil moderate'][i]])
    return user_liberal, user_moderate

def topn(data_test,data_prediction,data_prediction_hybrid,n,file):
    test = pd.read_csv(os.path.join(os.path.dirname(__file__), data_test), delimiter=",", quoting=3)
    prediction = pd.read_csv(os.path.join(os.path.dirname(__file__), data_prediction), delimiter=",", quoting=3)
    prediction_hybrid = pd.read_csv(os.path.join(os.path.dirname(__file__), data_prediction_hybrid), delimiter=",", quoting=3)
    user_cf, user_kbs = prediksi_user_cf_kbs(prediction)
    user=data_test_user(test)
    user_liberal,user_moderate=prediksi_liberal_moderate(prediction_hybrid)
    jumlah_kbs=0
    jumlah_cf=0
    jumlah_liberal=0
    jumlah_moderate=0
    f_cf = open(file + 'cf.csv', 'wb')
    cf_file = csv.writer(f_cf)
    cf_file.writerow(('user', 'item', 'hasil cf', 'real'))
    f_kbs = open(file + 'kbs.csv', 'wb')
    kbs_file = csv.writer(f_kbs)
    kbs_file.writerow(('user', 'item', 'hasil kbs', 'real'))
    f_liberal = open(file + 'liberal.csv', 'wb')
    liberal_file = csv.writer(f_liberal)
    liberal_file.writerow(('user', 'item', 'hasil liberal', 'real'))
    f_moderate = open(file + 'moderate.csv', 'wb')
    moderate_file = csv.writer(f_moderate)
    moderate_file.writerow(('user', 'item', 'hasil moderate', 'real'))
    for i in user:
        a = sorted(user_kbs[i], key=lambda x: x[2], reverse=True)
        user_choice_kbs = a[:n]
        b = sorted(user_cf[i], key=lambda x: x[2], reverse=True)
        user_choice_cf = b[:n]
        c = sorted(user_liberal[i], key=lambda x: x[2], reverse=True)
        user_choice_liberal = c[:n]
        d = sorted(user_moderate[i], key=lambda x: x[2], reverse=True)
        user_choice_moderate = d[:n]

        for k in user_choice_kbs:
            for j in user[i]:
                if j[1] == k[1]:
                    print "berhasil"
                    jumlah_kbs += 1
                    kbs_file.writerow((i, j[1], k[2], j[2]))

        for k in user_choice_cf:
            for j in user[i]:
                if j[1] == k[1]:
                    print "berhasil cf"
                    jumlah_cf += 1
                    cf_file.writerow((i, j[1], k[2], j[2]))

        for k in user_choice_liberal:
            for j in user[i]:
                if j[1] == k[1]:
                    print "berhasil liberal"
                    jumlah_liberal += 1
                    liberal_file.writerow((i, j[1], k[2], j[2]))

        for k in user_choice_moderate:
            for j in user[i]:
                if j[1] == k[1]:
                    print "berhasil moderate"
                    jumlah_moderate += 1
                    moderate_file.writerow((i, j[1], k[2], j[2]))

        print jumlah_liberal
        print jumlah_moderate
        print jumlah_cf
        print jumlah_kbs
def hit_rate(data_test,data_prediction,data_prediction_hybrid,n,file):
    test = pd.read_csv(os.path.join(os.path.dirname(__file__), data_test), delimiter=",", quoting=3)

for i in [1,3,5,15,25,50]:
    topn('data test_15.csv','hasil_allprediction_15item_15user.csv.csv','hasil_hybrid_15.csv',i,'hasil_top_'+str(i)+'_15')

