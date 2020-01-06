# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:28:20 2020

@author: Administrator
"""

#载入接下来分析用的库
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.recurrent import LSTM, GRU
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.embeddings import Embedding
from keras.layers.normalization import BatchNormalization

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
import matplotlib.pyplot as plt
%matplotlib inline

path = 'D:/Notebook/_文本分类/NLP文本分类算法集锦_从入门到精通/'
os.chdir(path)
data = pd.read_excel('./复旦大学中文文本分类语料.xlsx','Sheet1')

data.head()

data.info()

data.分类.unique()

import jieba

data['文本分词'] = data['正文'].apply(lambda x:jieba.cut(x) )
type(data.文本分词[1])
data['文本分词'] =[' '.join(x) for x in data['文本分词']]

data.head()

# 用scikit-learn中的LabelEncoder将文本标签（分类）转化为数字(int)
lbl_enc = preprocessing.LabelEncoder()
y = lbl_enc.fit_transform(data.分类.values)

# 用scikit-learn的model_selection模块中的train_test_split
# 来拆分训练集和测试集
# stratify = y 参数解释：
# stratify 参数拆分训练集和测试集的时候保证train、test集合中各个分类的比例基本保持一致
x_train, x_test, y_train, y_test = train_test_split(data.文本分词.values, y,
                                                  stratify = y,
                                                  random_state=42,
                                                  test_size=0.1, shuffle=True)
print (x_train.shape)
print (y_train.shape)
print (x_test.shape)
print (y_test.shape)


X=data['文本分词']
X=[i.split() for i in X]
# 训练word2vec词向量:
import gensim
# X是经分词后的文本构成的list，也就是tokens的列表的列表
model = gensim.models.Word2Vec(X,min_count =5,window =8,size=100)
embeddings_index = dict(zip(model.wv.index2word, model.wv.vectors))

print('发现 %s 个词向量.' % len(embeddings_index))

model['汽车']

stopwords_list=[line.strip() for line in open('./停用词表.txt','r',
                encoding='utf-8').readlines()]
def sent2vec(s):
    words = s.split(' ')
    words = [w for w in words if not w in stopwords_list]
    M = []
    for w in words:
        try:
            #M.append(embeddings_index[w])
            M.append(model[w])
        except:
            continue
    M = np.array(M)
    v = M.sum(axis=0)
    if type(v) != np.ndarray:
        return np.zeros(300)
    return v / np.sqrt((v ** 2).sum())

x_train_w2v = [sent2vec(x) for x in tqdm(x_train)]
x_test_w2v = [sent2vec(x) for x in tqdm(x_test)]

x_train_w2v = np.array(x_train_w2v)
x_test_w2v = np.array(x_test_w2v)

# 在使用神经网络前，对数据进行去均值方差归一化
scl = preprocessing.StandardScaler()
x_train_w2v_scl = scl.fit_transform(x_train_w2v)
x_test_w2v_scl = scl.transform(x_test_w2v)

# 对标签进行binarize处理
y_train_enc = np_utils.to_categorical(y_train)
y_test_enc = np_utils.to_categorical(y_test)

#创建1个3层的顺序神经网络（Sequential Neural Net）
model = Sequential()

model.add(Dense(300, input_dim=100, activation='relu'))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(Dense(300, activation='relu'))
model.add(Dropout(0.3))
model.add(BatchNormalization())

model.add(Dense(20))
model.add(Activation('softmax'))

# 模型编译
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.summary()

model.fit(x_train_w2v_scl, y=y_train_enc, batch_size=64,
          epochs=5, verbose=1,
          validation_data=(x_test_w2v_scl, y_test_enc))

