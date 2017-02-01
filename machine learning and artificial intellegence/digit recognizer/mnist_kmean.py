import numpy
import matplotlib
import matplotlib.pyplot
import struct
import os
import collections
import random

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


def euclidian_distance(point,cluster):
    return numpy.sqrt(numpy.sum((numpy.array(point)-numpy.array(cluster))**2))

def search_centroid(image):
    return numpy.mean(image,axis=0,dtype=numpy.int)

def nearest_cluster(point,cluster_p):
    d=euclidian_distance(point,cluster_p[0])
    index=0
    for i in range(len(cluster_p)):
        distance=euclidian_distance(point,cluster_p[i])
        if (distance<d):
            index =i
            d=distance
    return index

def createrandcentroid(image,c):
    centroid=[]
    for i in c:
        centroid.append(image[i])
    return centroid

def createeveryclass(label,c):
    l=[]
    j=[]
    for i in range(len(label)):
        if label[i] not in l:
            l.append(label[i])
    return l

def clustering(image,cluster_p):
    c = random.sample(range(0, image.shape[0]), cluster_p)
    centroid = createrandcentroid(image, c)
    prev=[]
    j=0
    while(numpy.array_equal(centroid,prev)!=True):
        j+=1
        print j
        cluster=collections.defaultdict(list)
        for i in image:
            cluster[nearest_cluster(i,centroid)].append(i)
        prev=centroid
        centroid=[]
        for i in cluster:
            centroid.append(search_centroid(cluster[i]))
    '''
    for i in xrange(len(centroid)):
        plt.subplot(int(numpy.ceil(len(centroid) / 5)), 5, i + 1)
        plt.imshow(centroid[i].reshape(28, 28))
    plt.show()
    '''
    visualize(numpy.array(centroid))
#rand
#image,label= read(500)
#clustering(image,10)
#10new
image,label= read(500)
clustering(image,20)