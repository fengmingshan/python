# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:04:57 2019

@author: Administrator
"""

from keras.layers.core import Activation, Dense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
from collections import Counter
import nltk
import numpy as np
import re
import os

data_path = 'D:/_python/python/机器学习_神经网络/文本分类/集团星火计划考题_英文影评分类'
os.chdir(data_path)

num_record = 0
max_length = 0
word_freq = Counter()

def clean_text(comment_text):
    comment_list = []
    for text in comment_text:
        # 将单词转换为小写
        text = text.lower()

        # 删除非字母、数字字符,注意标点符号要保留，因为标点符号也有意义
        text = re.sub(r"[^A-Za-z0-9(),!?@&$\t\'\`\"\_\n]", " ", text)
        text = re.sub(r"\n", " ", text)

        # 恢复常见的简写
        text = re.sub(r"what's", "what is ", text)
        text = re.sub(r"\'s", " ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"can't", "can not ", text)
        text = re.sub(r"cannot", "can not ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"i'm", "i am ", text)
        text = re.sub(r"\'re", " are ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)

        # 恢复特殊符号的英文单词
        text = text.replace('&', ' and')
        text = text.replace('@', ' at')
        text = text.replace('$', ' dollar')

        comment_list.append(text)
    return comment_list

with open('./data/train_data.txt',encoding = 'utf-8') as f:
    content = clean_text(f)
    for line in content:
        label,text = line.strip().split('\t')
        words = text.split(' ')
        if len(words) > max_length:
            max_length = len(words)
        for word in words:
            word_freq[word] += 1
        num_record += 1
print('记录数 : {} '.format(num_record))
print('最长语句 : {} '.format(max_length))
print('单词数量 : {}'.format(len(word_freq)))

vocabulary_size = 2508
MAX_TEXT_LENGTH = 43

word2index = {x:i+2 for i,x in enumerate(word_freq)}
index2word = {v:k for k, v in word2index.items()}

# 构造两个空数组用来装训练数据
X = np.empty(num_recs,dtype=list)
y = np.zeros(num_recs)

for i,line in enumerate(content):
    label,text = line.strip().split('\t')
    words = text.split(' ')
    seqs = []
    for word in words:
        seqs.append(word2index[word])
    X[i] = seqs
    y[i] = int(label)

# 将文本向量padding到最大长度
X = sequence.pad_sequences(X, maxlen=MAX_TEXT_LENGTH)
# 拆分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

# 建模
EMBEDDING_SIZE = 128
HIDDEN_LAYER_SIZE = 64
BATCH_SIZE = 32
NUM_EPOCHS = 10

model = Sequential()
model.add(Embedding(vocabulary_size, EMBEDDING_SIZE,input_length = MAX_TEXT_LENGTH))
model.add(LSTM(HIDDEN_LAYER_SIZE, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1))
model.add(Activation("sigmoid"))
model.compile(loss="binary_crossentropy", optimizer="adam",metrics=["accuracy"])
model.summary()

# 模型训练
model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS,validation_data=(X_test, y_test))
# 在测试集上验证
score, acc = model.evaluate(X_test, y_test, batch_size=BATCH_SIZE)
print("\nTest score: %.3f, accuracy: %.3f" % (score, acc))

# 随机抽取10条测试样本进行测试
print('{}   {}      {}'.format('预测','真实','语句'))
for i in range(10):
    idx = np.random.randint(len(Xtest))
    xtest = X_test[idx].reshape(1,43)
    ylabel = y_test[idx]
    ypred = model.predict(xtest)[0][0]
    sent = " ".join([index2word[x] for x in xtest[0] if x != 0])
    print(' {}      {}     {}'.format(int(round(ypred)), int(ylabel), sent))

# 自己写句子测试模型
INPUT_TEXT = ['What a bad film!','Wast my time to watch!',"Don't evaluation",'Awesome, worth the fare!',"Beyond my expectation!",'A boring night','Wast money.']
XX = np.empty(len(INPUT_TEXT), dtype=list)

i = 0
for sentence in INPUT_TEXT:
    words = sentence.lower().split(" ")
    #words = nltk.word_tokenize(sentence.lower())
    seq = []
    for word in words:
        if word in word2index:
            seq.append(word2index[word])
        else:
            seq.append(1)
    XX[i] = seq
    i += 1
# padding到最大长度43
XX = sequence.pad_sequences(XX, maxlen=MAX_TEXT_LENGTH)
labels = [int(round(x[0])) for x in model.predict(XX) ]
label2word = {1:'称赞', 0:'批评'}
for i in range(len(INPUT_TEXT)):
    print('{}   {}'.format(label2word[labels[i]], INPUT_TEXT[i]))

