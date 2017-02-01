import numpy
import matplotlib
import matplotlib.pyplot
import matplotlib.pyplot as plt
import struct
import os
from collections import Counter

def read(N):
    files = os.listdir(os.getcwd())
    image = open('train-images-idx3-ubyte', 'rb')
    label = open('train-labels-idx1-ubyte', 'rb')
    _, _ = struct.unpack('>II', label.read(8))
    labels = numpy.fromfile(label, dtype=numpy.int8)
    _, _, img_row, img_col = struct.unpack('>IIII', image.read(16))
    images = numpy.fromfile(image, dtype=numpy.uint8).reshape(len(labels), img_row * img_col)
    return images[0:N, :], labels[0:N]

def visualize(image):
    if image.ndim == 1:
        image = numpy.array([image])
    cols = int(numpy.ceil(numpy.sqrt(image.shape[0])))
    img_number = 0
    for row in xrange(0, cols):
        for col in xrange(0, cols):
            if img_number > image.shape[0] - 1:
                break
            else:
                ax = matplotlib.pyplot.subplot2grid((cols, cols), (row, col))
                ax.axes.axes.get_xaxis().set_visible(False)
                ax.axes.axes.get_yaxis().set_visible(False)
                imgplot = ax.imshow(image[img_number].reshape(28, 28), cmap=matplotlib.cm.Greys)
                imgplot.set_interpolation('nearest')
                ax.xaxis.set_ticks_position('top')
                ax.yaxis.set_ticks_position('left')
                img_number += 1
    matplotlib.pyplot.show()

X,Y=read(1000)
def eig_plot(eig_vals):
    hasil=[]
    s=numpy.sum(numpy.absolute(eig_vals))
    j =numpy.sum(numpy.absolute(eig_vals[:64]))
    print (j/s)*100
    '''
    for i in eig_vals:
        hasil.append((numpy.sum(numpy.absolute(i))/s)*100)
    '''
    #plothasilerrornorm([i for i in range(len(eig_vals))],hasil)
    #plt.show()

def PCA(X,N):
    #visualize(X[:100])
    mean= numpy.mean(X.T,axis=0)
    nor =numpy.subtract(X.T,mean)
    cov=numpy.cov(nor)
    eig_vals, eig_vecs = numpy.linalg.eig(cov)
    #visualize(numpy.matrix(eig_vecs.T)[:64].real)
    eig_space=numpy.dot(eig_vecs.T[:N],X.T)
    data=numpy.dot(eig_space.T,eig_vecs.T[:N])
    #eig_plot(eig_vals)
    #visualize(numpy.matrix(data[:100]).real)
    return data

def euclidian_distance(x,y):
    return numpy.sqrt(numpy.sum((numpy.array(x)-numpy.array(y))**2))

def knn(train,test,k,label):
    neighbor=[]
    kn=[]
    for i in range(len(train)):
        x= euclidian_distance(train[i],test)
        neighbor.append([x,i,label[i]])
    neighbor = sorted(neighbor, key=lambda n: n[0])
    if(neighbor[0][0]==0.0):
        del neighbor[0]
    for i in range(k):
        kn.append([neighbor[i][1],neighbor[i][2]])
    return kn

def knn_class(knn):
    label=numpy.array(knn).T.tolist()
    l=label[1]
    c=Counter(l)
    return c.most_common(1)

def knn_all(train,test,k,label):
    error=0
    all=[]
    for i in range(len(test)):
        lis= knn(train,test[i],k,label)
        c=knn_class(lis)
        if(c[0][0] !=label[i]):
            error+=1
        #all.append([lab[i][0],test[i][1],c])
    e= error*1.0/len(test)*1.0
    return e

def plothasilerrornorm(k_coba, hasil_error):
    plt.plot([k for k in k_coba],[kn for kn in hasil_error], 'bo-',c='green',label='KNN')
#visualize(X[:100])
#PCA(X,64)

hasil=[]
k_coba=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195,200]
for i in k_coba:
    hasil.append(knn_all(PCA(X,i),PCA(X,i),15,Y[:1000]))
'''
plothasilerrornorm(k_coba,hasil)
plt.title("Hasil error missclasification KNN ")
plt.legend(loc="upper right")
plt.show()
'''