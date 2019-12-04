# -*- coding: utf-8 -*-
"""
Created on  2018/5/23 20:41
 lstm用来做英文的情感分类
 https://blog.csdn.net/william_2015/article/details/72978387
@author: lhua
"""
from keras.layers.core import Activation, Dense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
import collections
import nltk
import numpy as np

import os

data_path = 'D:/_python/python/机器学习_神经网络/文本分类/LSTM_word2vec文本分类'
os.chdir(data_path)


# 计算文本的最大长度，并创建词频字典
maxlen = 0
# 这里使用collections.Counter()替代字典来创建词频字典，如果使用普通字典，加入新词操作很麻烦
# 另外后面要用到统计词频最高的前2000个词，只有collections.Counter()有这个功能
word_freqs = collections.Counter()
num_recs = 0
with open('./data/emotion_english_traindata.txt','r+',encoding='utf-8') as f:
    for line in f:
        label, sentence = line.strip().split("\t")
        #words = nltk.word_tokenize(sentence.lower())
        words = sentence.lower().split(' ')
        if len(words) > maxlen:
            maxlen = len(words)
        for word in words:
            word_freqs[word] += 1
        num_recs += 1
print('max_len ', maxlen)
print('nb_words ', len(word_freqs))
print('num_recs ', num_recs)

# prepare the data
MAX_FEATURES = 2000
MAX_SENTENCE_LENGTH = 40
# 词汇大小设置成 2000+2，因为后面还要添加一个Null词,最后对文本向量进行padding时还会添加一个0，总共就是2002
vocab_size = min(MAX_FEATURES, len(word_freqs)) + 2
# 构造word2index的字典，这里只取了词频字典里排在前2000的词，因为词频较小的词对于预测没有价值可以忽略
# .most_common返回的是一个元组组成的list('green', 3)
# x[0]是词，x[1]是词频，i表示词频的排名从0开始，x+2变成从2开始。因为1要用给Null词用
word2index = {x[0]: i+2 for i, x in enumerate(word_freqs.most_common(MAX_FEATURES))}
word2index["Null"] = 1
# k，v取反构造index2word的字典，
index2word = {v:k for k, v in word2index.items()}

# 构造两个空数组用来装训练数据
X = np.empty(num_recs,dtype=list)
y = np.zeros(num_recs)

# 重新读取源文件，这次将词直接转index，并将词index放入X,label放入y中
i = 0
with open('./data/emotion_english_traindata.txt','r+',encoding='utf-8') as f:
    for line in f:
        label, sentence = line.strip().split("\t")
        words = sentence.lower().split(" ")
        #words = nltk.word_tokenize(sentence.lower())
        seqs = []
        for word in words:
            if word in word2index:
                seqs.append(word2index[word])
            else:
                # 如果这个词不是2000个高频词，那么直接把他替换成Null词，编号为1
                # 最后对文本向量进行pad时还会补0，那么总的词号就是从0——2001,共2002个
                seqs.append(word2index["Null"])
        X[i] = seqs
        y[i] = int(label)
        i += 1
# 最后得到的词向量
X[0]
# pad the sequence to the same length
X = sequence.pad_sequences(X, maxlen=MAX_SENTENCE_LENGTH)
# divide the test set and training set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# build the network
EMBEDDING_SIZE = 128
HIDDEN_LAYER_SIZE = 64
BATCH_SIZE = 32
NUM_EPOCHS = 10
model = Sequential()
model.add(Embedding(vocab_size, EMBEDDING_SIZE,input_length=MAX_SENTENCE_LENGTH))
model.add(LSTM(HIDDEN_LAYER_SIZE, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1))
model.add(Activation("sigmoid"))
model.compile(loss="binary_crossentropy", optimizer="adam",metrics=["accuracy"])
model.summary()
# network training
model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS,validation_data=(X_test, y_test))
# verify on the test set
score, acc = model.evaluate(X_test, y_test, batch_size=BATCH_SIZE)
print("\nTest score: %.3f, accuracy: %.3f" % (score, acc))

print('{}   {}      {}'.format('预测','真实','语句'))
for i in range(5):
    idx = np.random.randint(len(Xtest))
    xtest = X_test[idx].reshape(1,40)
    ylabel = y_test[idx]
    ypred = model.predict(xtest)[0][0]
    sent = " ".join([index2word[x] for x in xtest[0] if x != 0])
    print(' {}      {}     {}'.format(int(round(ypred)), int(ylabel), sent))

# 自己创建语句进行测试
INPUT_SENTENCES = ['I love reading.','You are a bitch.']
XX = np.empty(len(INPUT_SENTENCES), dtype=list)

i = 0
for sentence in INPUT_SENTENCES:
    words = sentence.lower().split(" ")
    #words = nltk.word_tokenize(sentence.lower())
    seq = []
    for word in words:
        if word in word2index:
            seq.append(word2index[word])
        else:
            seq.append(word2index['UNK'])
    XX[i] = seq
    i += 1
# build a sequence of the same length
XX = sequence.pad_sequences(XX, maxlen=MAX_SENTENCE_LENGTH)
labels = [int(round(x[0])) for x in model.predict(XX) ]
label2word = {1:'积极', 0:'消极'}
for i in range(len(INPUT_SENTENCES)):
    print('{}   {}'.format(label2word[labels[i]], INPUT_SENTENCES[i]))