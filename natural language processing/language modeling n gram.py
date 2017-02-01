import re
# import nltk
# nltk.download()
from nltk.util import ngrams
from collections import Counter
import copy
from decimal import *

with open("wikipedia2text-extracted.txt") as f:
    content = f.readlines()
teks = ''.join(content)

# cleaning
teks = re.sub('<.*>', '', teks)
teks = re.sub('\(.*\)', '', teks)
teks = re.sub('(\d+(?:th|s|(,\d+)+|(.\d+)+%)|\d+)', 'number', teks)
teks = re.sub('[^\w\s.]', ' ', teks)
teks = re.sub('(\s+|\n)', ' ', teks)

# normalizing
data = ""
sentence_list = re.split('\.',teks)
for sentence in sentence_list:
    if(sentence.strip()!=''):
        sentence = re.sub('(\s+|\n)',' ',re.sub(r'(.*)', r'<s> \1 </s> ', sentence))
        data += sentence.lower()

train = '<s>'.join(data.split('<s>')[:-10])[:-1]
test = ''.join(data.split('<s>')[-20:])[1:-6]
list_test = test.split(' </s>  ')

# print train
# print '-----------'
# print test
# print '-----------'
# print list_test

#fungsi unigram
def unigram(used_token, sentence):
    #persiapan unigram token
    token = copy.deepcopy(used_token)
    token = [word for word in token if word != '<s>']
    unigrams = ngrams(token, 1)
    hasil = Counter(unigrams)

    sentence = re.split(' ',sentence) + ['</s>']
    print 'Unigram model\n====================================================='
    print 'wi\tC(wi)\t#words\tP(wi)\n====================================================='
    n = len(token)
    prob_sentence = Decimal(1)
    for word in sentence:
        if hasil[(word,)]==0: #mengatasi unknown word <unk>
            prob_word = Decimal(1.0/n)
            print '<unk>', '\t', '1', '\t', n, '\t', prob_word
        else:
            prob_word = Decimal(hasil[(word,)]*1.0/n)
            print word, '\t', hasil[(word,)], '\t', n, '\t', prob_word
        prob_sentence *= prob_word
    print '====================================================='
    print 'Prob. unigrams: ', prob_sentence
    print 'Perplexity: ', pow(1 / prob_sentence, Decimal(1.0/len(sentence)))

#fungsi bigram MLE
def bigram(used_token, sentence):
    #persiapan bigram token dan unigram token
    token = copy.deepcopy(used_token)
    unigrams = ngrams(token, 1)
    hasil_unigram = Counter(unigrams)
    bigrams = ngrams(token, 2)
    hasil = Counter(bigrams)

    sentence = ['<s>'] + re.split(' ',sentence) + ['</s>']
    print 'Bigram model\n====================================================='
    print 'wi\twi+1\tCi,i+1\tC(i)\tP(wi+1|wi)\n====================================================='
    prob_sentence = 1
    for i in xrange(len(sentence)-1):
        prob_word = Decimal(hasil[(sentence[i],sentence[i+1])] * 1.0) / Decimal(hasil_unigram[(sentence[i],)])
        prob_sentence *= prob_word
        print sentence[i], '\t', sentence[i+1], '\t', hasil[(sentence[i],sentence[i+1])], '\t', hasil_unigram[(sentence[i],)], '\t', prob_word
    print '====================================================='
    print 'Prob. unigrams: ', prob_sentence
    print 'Perplexity: ', pow(1 / prob_sentence, Decimal(1.0 / len(sentence)))

#fungsi bigram
def bigram_smoothed(used_token, sentence):
    #persiapan bigram token
    token = copy.deepcopy(used_token)
    unigrams = ngrams(token, 1)
    hasil_unigram = Counter(unigrams)
    bigrams = ngrams(token, 2)
    hasil = Counter(bigrams)

    sentence = ['<s>'] + re.split(' ',sentence) + ['</s>']
    print 'Bigram model\n====================================================='
    print 'wi\twi+1\tCi,i+1\tC(i)\tP(wi+1|wi)\n====================================================='
    prob_sentence = Decimal(1)
    v = pow(len(set(token)),2)
    for i in xrange(len(sentence)-1):
        prob_word = Decimal(Decimal(hasil[(sentence[i],sentence[i+1])] * 1.0 + 1.0) / Decimal(hasil_unigram[(sentence[i],)] + v))
        prob_sentence *= prob_word
        print sentence[i], '\t', sentence[i+1], '\t', hasil[(sentence[i],sentence[i+1])], '\t', hasil_unigram[(sentence[i],)], '\t', prob_word
    print '====================================================='
    print 'Prob. bigrams: ', prob_sentence
    print 'Perplexity: ', pow(1 / prob_sentence, Decimal(1.0 / (len(sentence)-1)))

token = re.split(' ',train)
token = [word for word in token if word != '']
# print token
print '------------  UNIGRAM  ------------'
unigram(token,'the propaganda can message any government')
print '------------------------------------------'
for sentence in list_test:
    unigram(token,sentence)
    print
print '\n\n'
print '------------  BIGRAM  ------------'
bigram_smoothed(token,'the propaganda can message any government')
print '------------------------------------------'
for sentence in list_test:
    bigram_smoothed(token,sentence)
    print