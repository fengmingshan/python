# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:28:20 2020

@author: Administrator
"""

# 载入接下来分析用的库
import pandas as pd
import numpy as np
import os
import gensim
import jieba
from tqdm import tqdm
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.recurrent import LSTM, GRU
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.embeddings import Embedding
from keras.layers import GlobalMaxPooling1D, Conv1D, MaxPooling1D, Flatten, Bidirectional, SpatialDropout1D
from keras.callbacks import EarlyStopping
from keras.preprocessing import sequence, text

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
%matplotlib inline

path = 'D:/Notebook/_文本分类/NLP文本分类算法集锦_从入门到精通/'
os.chdir(path)
data = pd.read_excel('./复旦大学中文文本分类语料.xlsx', 'Sheet1')

data.head()

data.info()

data.分类.unique()

stopwords_list = [line.strip() for line in open('./停用词表.txt', 'r',
                  encoding='utf-8').readlines()]

data['文本分词'] = data['正文'].apply(lambda x: jieba.cut(x))
data['文本分词'] = [' '.join(x) for x in data['文本分词'] if x not in stopwords_list]

data.head()
data['文本分词'][0]

# 用scikit-learn中的LabelEncoder将文本标签（分类）转化为数字(int)
lbl_enc = preprocessing.LabelEncoder()
y = lbl_enc.fit_transform(data.分类.values)

# 用scikit-learn的model_selection模块中的train_test_split
# 来拆分训练集和测试集
# stratify = y 参数解释：
# stratify 参数拆分训练集和测试集的时候保证train、test集合中各个分类的比例基本保持一致
x_train, x_test, y_train, y_test = train_test_split(data.文本分词.values, y,
                                                    stratify=y,
                                                    random_state=42,
                                                    test_size=0.1, shuffle=True)
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)


X = data['文本分词']
X = [i.split() for i in X]
# 训练word2vec词向量:
# X是经分词后的文本构成的list，也就是tokens的列表的列表
'''
Word2Vec参数说明:
min_count : 忽略词频小于此值的单词。
window : 一个句子中当前单词和被预测单词的最大距离。
size : word向量的维度
sg : 模型的训练算法: 0:CBOW , 1:skip-gram
cbow_mean : 0: 使用上下文单词向量的总和; 1: 使用均值，当使用CBOW训练算法时才有效。
'''
model = gensim.models.Word2Vec(X, min_count=5, window=8, size=100)

embeddings_index = dict(zip(model.wv.index2word, model.wv.vectors))

print('发现 %s 个词向量.' % len(embeddings_index))

model['汽车']

# 使用 keras tokenizer
token = text.Tokenizer(num_words=None)
max_len = 100

token.fit_on_texts(list(x_train) + list(x_test))
x_train_seq = token.texts_to_sequences(x_train)
x_test_seq = token.texts_to_sequences(x_test)

word_index = token.word_index

# 对文本序列进行zero填充
x_train_pad = sequence.pad_sequences(x_train_seq, maxlen=max_len)
x_test_pad = sequence.pad_sequences(x_test_seq, maxlen=max_len)

# 对标签进行binarize处理
y_train_enc = np_utils.to_categorical(y_train)
y_test_enc = np_utils.to_categorical(y_test)


# 基于已有的数据集中的词汇创建一个词嵌入矩阵（Embedding Matrix）
embedding_matrix = np.zeros((len(word_index) + 1, 100))
for word, i in tqdm(word_index.items()):
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

# 基于前面训练的Word2vec词向量，构建1个2层的GRU模型
model = Sequential()
model.add(Embedding(len(word_index) + 1,
                     100,
                     weights=[embedding_matrix],
                     input_length=max_len,
                     trainable=False))
model.add(SpatialDropout1D(0.3))
model.add(GRU(100, dropout=0.3, recurrent_dropout=0.3, return_sequences=True))
model.add(GRU(100, dropout=0.3, recurrent_dropout=0.3))

model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.8))

model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.8))

model.add(Dense(20))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

#在模型拟合时，使用early stopping这个回调函数（Callback Function）
earlystop = EarlyStopping(monitor='val_loss', min_delta=0, patience=3, verbose=0, mode='auto')
model.fit(x_train_pad, y=y_train_enc, batch_size=512, epochs=20,
          verbose=1, validation_data=(x_test_pad, y_test_enc), callbacks=[earlystop])