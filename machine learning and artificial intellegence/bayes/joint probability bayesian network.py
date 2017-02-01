import itertools
import copy
dag = {'A': [], 'B': ['A'], 'C': ['A'], 'D': ['B', 'C'], 'E': ['C']}

A=[[['T'],0.6],[['F'],0.4]]
B=[[['T','T'],0.2],[['T','F'],0.75],[['F','T'],0.8],[['F','F'],0.25]]
C=[[['T','T'],0.8],[['T','F'],0.1],[['F','T'],0.2],[['F','F'],0.9]]
D=[[['T','T','T'],0.95],[['T','T','F'],0.9],[['T','F','T'],0.8],[['T','F','F'], 0.00001],[['F','T','T'],0.05]
,[['F','T','F'],0.1],[['F','F','T'],0.2],[['F','F','F'],0.99999]]
E=[[['T','T'],0.7],[['T','F'],0.00001],[['F','T'],0.3],[['F','F'],0.99999]]

trans={'A':A,'B':B,'C':C,'D':D,'E':E}
join={'A':'T','B':'T'}

def search_prob(var,prob):
    for i in trans[var]:
        if i[0]==prob:
            return i[1]

def joint_func_inference(join):
    comb_prob={}
    for i in dag.keys():
        tmp=[]
        tmp.append(join[i])
        for j in dag[i]:
            tmp.append(join[j])
        comb_prob[i]=tmp
    hasil=1
    for i in comb_prob.keys():
        hasil *= search_prob(i,comb_prob[i])
    return hasil

def create_join(cari,jumlah_var):
    daftar_combination=[]
    for combination in itertools.product(['T', 'F'], repeat=jumlah_var-len(cari.keys())):
        i = 0
        tmp = copy.deepcopy(cari)
        for var in dag.keys():
            if var not in cari:
                tmp.update({var:combination[i]})
                i+=1
        daftar_combination.append(tmp)
    return daftar_combination

def join_all(combination_join):
    hasil=0
    for i in combination_join:
        hasil += joint_func_inference(i)
    return hasil

def conditional(cari,given):
    cari.update(given)
    hasil = join_all(create_join(cari,5)) / join_all(create_join(given,5))
    return hasil

def count_solusion(soal):
    print 'P(',soal,') =',
    if '|' in soal:
        soal = soal.split('|')
        cari = {i[0]: i[2] for i in soal[0].split(',')}
        given = {i[0]: i[2] for i in soal[1].split(',')}
        print conditional(cari, given)

count_solusion('B=T|A=F,C=F,E=T')    # 1
count_solusion('C=T|D=T,A=F')        # 2
count_solusion('A=T|D=T,C=F')        # 3
count_solusion('A=T|E=T')            # 4
count_solusion('E=T|A=T')            # 5
count_solusion('A=T|D=T')            # 6
count_solusion('D=T|A=T')            # 7
count_solusion('B=T|E=T')            # 8
count_solusion('B=T|E=T,A=T')        # 9
count_solusion('E=T,A=T,D=T|B=T')    # 10
