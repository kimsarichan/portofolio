from  collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import math
import re

with open("wikipedia2text-extracted.txt") as f:
    content = f.readlines()
print content

delimiters = ['\n',' ','"','"','(',')','[',']','-', ',', '.', '?', '!', ':',';']
words = content
for delimiter in delimiters:
    new_words = []
    for word in words:
        if word !="":
            word= word.lower()
            if(word.isdigit() == False):
                new_words += word.split(delimiter)
    words = new_words
hasil= Counter(words)
a= hasil.most_common(10)
print a
print dict(sorted(hasil.items(), key=lambda i: i[1])[:10]) #less common
plt.subplot(121)
plt.plot([i for i in xrange(len(hasil))], sorted(hasil.values(), reverse=True), 'b-')
plt.subplot(122)
plt.plot([i for i in xrange(len(hasil))], [math.log10(i) for i in sorted(hasil.values(), reverse=True)], 'b-')
#plt.xticks(range(len(hasil)))
plt.show()
