import math
import numpy as np
import random
import matplotlib.pyplot as plt
class Data(object):
    def __init__(self):
        self.demand={0:0,1:19,2:21,3:6,4:19,5:7,6:12,7:16,8:6,9:16,10:8,11:14,12:21,13:16,14:3,15:22,16:18,17:19,
                 18:1,19:24,20:8,21:12,22:4,23:8,24:24,25:24,26:2,27:20,28:15,29:2,30:14,31:9}
        self.posisi={0:[82,76],1:[96,44],2:[50,5],3:[49,8],4:[13,7],5:[29,89],6:[58,30],7:[84,39],8:[14,24]
                     ,9:[2,39],10:[3,82],11:[5,10],12:[98,52],13:[84,25],14:[61,59],15:[1,65],16:[88,51],17:[91,2],
                     18:[19,32],19:[93,3],20:[50,93],21:[98,14],22:[5,42],23:[42,9],24:[61,62],25:[9,97],26:[80,55],
                     27:[57,69],28:[23,15],29:[20,70],30:[85,60],31:[98,5]}
    def eulidian(self,x,y):
        return math.sqrt(((((self.posisi[x][0]-self.posisi[y][0])))*((self.posisi[x][0]-self.posisi[y][0])))+
                         ((((self.posisi[x][1]-self.posisi[y][1])))*((self.posisi[x][1]-self.posisi[y][1]))))

class Individu(object):
    def __init__(self, jmlBit=31):
        self.kromosom=self.make_kromosom(jmlBit)
        self.fitness=0
        self.data=Data()

    def make_kromosom(self,jmlbit):
        return [i+1 for i in np.random.permutation(jmlbit).tolist()]

    def calculate_fitness(self):
        depot=100
        fit=0
        prev=0
        for i in range(len(self.kromosom)):
            if(depot >= self.data.demand[self.kromosom[i]]):
                depot-=self.data.demand[self.kromosom[i]]
                fit+=self.data.eulidian(self.kromosom[i],prev)
                prev=self.kromosom[i]
            else:
                depot=100
                fit+=self.data.eulidian(prev,0)+self.data.eulidian(self.kromosom[i],0)
                depot-=self.data.demand[self.kromosom[i]]
                prev=self.kromosom[i]
        fit+=self.data.eulidian(prev,0)
        return fit

    def jalur(self):
        s=self.kromosom
        hasil=[]
        hasil.append(0)
        depot=100
        for i in range(len(s)):
            if(depot >= self.data.demand[s[i]]):
                depot-=self.data.demand[s[i]]
                hasil.append(s[i])
            else:
                depot=100
                hasil.append(0)
                depot-=self.data.demand[s[i]]
                hasil.append(s[i])
        hasil.append(0)
        return hasil

class Populasi(object):
    def __init__(self,mutationrate=0.1):
        self.populasi=[]
        self.mutationrate=mutationrate

    def inisialisasi_populasi(self,jmlpopulasi):
        self.jmlpopulasi=jmlpopulasi
        for i in range(jmlpopulasi):
            i = Individu()
            self.populasi.append([i.kromosom,i.calculate_fitness()])

    def bestindividu(self):
        tmp=self.populasi
        a = min(tmp, key=lambda n: n[1])
        return a

    def chooseparent(self):
        #roulette wheel
        weight=sum(ind[1] for ind in self.populasi)
        n=np.random.uniform(0,weight)
        for ind in self.populasi:
            if n < ind[1]:
                return  ind
            n=n-ind[1]

    def crossover(self,parent1, parent2):
        #single point crossover
        a=np.random.randint(1,31)
        anak1=parent1[0:a]
        anak2=parent2[0:a]
        for i in parent2:
            if i not in anak1:
                anak1.append(i)
        for i in parent1:
            if i not in anak2:
                anak2.append(i)
        a1=Individu()
        a1.kromosom=anak1
        a2=Individu()
        a2.kromosom=anak2
        return [[a1.kromosom,a1.calculate_fitness()],[a2.kromosom,a2.calculate_fitness()]]

    def mutation(self,sw):
        #swap mutation
        n=random.uniform(0,1)
        if n<=self.mutationrate:
            swap=np.random.permutation(np.arange(30))[:2]
            temp=sw[0][swap[0]:swap[0]+1]
            sw[0][swap[0]:swap[0]+1]=sw[0][swap[1]:swap[1]+1]
            sw[0][swap[1]:swap[1]+1]=temp
        return sw


class GA(object):
    def __init__(self):
        self.generasi = None
        self.stagnant=10000

    def seleksisurvivor(self,pop):
        pop_baru = Populasi()
        pop_baru.populasi.append(pop.bestindividu())
        for i in range(len(pop.populasi)/2):
            parent1=pop.chooseparent()
            parent2=pop.chooseparent()
            anak = pop.crossover(parent1[0],parent2[0])
            anak1 = pop.mutation(anak[0])
            anak2 = pop.mutation(anak[1])
            pop_baru.populasi.append(anak1)
            pop_baru.populasi.append(anak2)
        self.generasi = pop_baru

    def solve(self):
        p = Populasi()
        p.inisialisasi_populasi(11)
        self.generasi = p
        plot=[]
        n=0
        i=1
        last=self.generasi.bestindividu()[1]
        while(n<self.stagnant):
            print "generasi ke- ",i
            print "best individu : ", self.generasi.bestindividu()[0]," fitness :",self.generasi.bestindividu()[1]
            if(self.generasi.bestindividu()[1]==last):
                n+=1
            else:
                last=self.generasi.bestindividu()[1]
                n=0
            plot.append(self.generasi.bestindividu()[1])
            self.seleksisurvivor(self.generasi)
            i+=1
        i=Individu()
        i.kromosom=self.generasi.bestindividu()[0]
        print i.jalur()
        plt.plot([kn for kn in plot],'b-',c='red')
        plt.show()

g=GA()
g.solve()


