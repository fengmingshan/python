# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 09:47:33 2019

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:28:25 2019

@author: Administrator
"""
# 载入接下来分析用的库
import itertools
import matplotlib.pyplot as plt
import gensim
import pandas as pd
import numpy as np
import os
import jieba
from tqdm import tqdm
from keras.models import load_model
from keras.utils import np_utils
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.normalization import BatchNormalization
from keras.layers.recurrent import LSTM, GRU
from keras.layers import GlobalMaxPooling1D, Conv1D, MaxPooling1D, Flatten, Bidirectional, SpatialDropout1D
from keras.models import Sequential
from keras.layers import Input
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence, text
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# 定义损失评估函数
data_path = 'D:/Notebook/通过机器学习进行投诉分类'
os.chdir(data_path)

df1 = pd.read_excel('train-test-ts-V2.xls', sheetname='训练集1')  # 数据类型：DataFrame
df2 = pd.read_excel('train-test-ts-V2.xls', sheetname='测试集1')  # 数据类型：DataFrame
df = df1.append(df2)  # 把两个DataFrame拼接起来，方便进行数据预处理
df.head(5)
df.columns
df.loc[0, '文本']
print(len(df))
print(len(df1))
print(len(df2))

# 去除文本中的一些网页格式
df['文本'] = df['文本'].map(lambda x: x.replace('①', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('②', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('③', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('④', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('⑤', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('【', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('】', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('(', ''))
df['文本'] = df['文本'].map(lambda x: x.replace(')', ''))
df['文本'] = df['文本'].map(lambda x: x.replace(':', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('<br>', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('<b>', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('</b>', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('\n', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('-', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('>', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('：', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('；', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('.', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('（', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('）', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('，', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('。', ''))
df['文本'] = df['文本'].map(lambda x: x.replace('、', ''))

# 去除文本中的数字串


def replace_num(text):
    import re
    p1 = r"[0-9]+"  # 这是我们写的正则表达式规则，你现在可以不理解啥意思
    pattern1 = re.compile(p1)  # 我们在编译这段正则表达式
    res = pattern1.findall(text)
    res.sort(key=lambda i: len(i), reverse=True)
    if len(res) > 0:  # 如果匹配成功
        for i in range(len(res)):
            new_text = text.replace(res[i], '')  # 打印出来
            text = new_text
    return text


df['文本'] = df['文本'].map(lambda x: replace_num(x))


# 定义停词函数
def loadStopWords():
    stop = []
    for line in open('stopWord.txt').readlines():
        stop.append(line)
    return list(set(stop))

# 定义切词函数


def cutWords(msgs, stopWords):
    arr_leftWords = []
    for msg in msgs:
        seg_list = jieba.cut(msg, cut_all=False)
        # key_list = jieba.analyse.extract_tags(msg,20) #get keywords
        #leftWords = []
        leftWords = ''
        for i in seg_list:  # for i in y,y可以是列表、元组、字典、Series
            if (i not in stopWords):
                leftWords += ' ' + i
        leftWords.strip()
        arr_leftWords.append(leftWords)
    return arr_leftWords


X = df['文本']
X[:5]

# 读取停用词表
stopwords = loadStopWords()
print(len(stopwords))
stopwords[:20]

# 对文本 X 进行分词操作
X_cut = cutWords(X, stopwords)
X_words_list = [x.split() for x in X_cut]

X_train, X_test, y_train, y_test = train_test_split(X_cut, df['标签'], test_size=0.15, random_state=0)
# print(X_train.shape,X_test.shape,y_train.shape,y_test.shape)

# =============================================================================
# 训练word2vec词向量:
# =============================================================================
# X_split是经分词后的文本构成的list，也就是tokens的列表的列表
#w2vModel = gensim.models.Word2Vec(X_words_list, min_count=5, window=8, size=100)
#embeddings_dict = dict(zip(w2vModel.wv.index2word, w2vModel.wv.vectors))
#print('共训练 %s 个词向量.' % len(embeddings_dict))
#w2vModel.save('w2vModel.model')

# 加载自己以前训练的词向量
w2vModel = gensim.models.Word2Vec.load('w2vModel.model')
embeddings_dict = dict(zip(w2vModel.wv.index2word, w2vModel.wv.vectors))

# 定义使用训练好的 w2vModel 模型，将全文本转词向量的函数
def sent2vec(s):
    words = str(s)
    M = []
    for w in words:
        try:
            # M.append(embeddings_index[w])
            M.append(w2vModel[w])
        except BaseException:
            continue
    M = np.array(M)
    v = M.sum(axis=0)
    if not isinstance(v, np.ndarray):
        return np.zeros(100)
    return v / np.sqrt((v ** 2).sum())

# 对训练集和验证集使用上述函数，进行文本向量化处理
# 这里使用了tqdm为迭代过程添加进度条
X_train_w2v = [sent2vec(x) for x in tqdm(X_train)]
X_test_w2v = [sent2vec(x) for x in tqdm(X_test)]

X_train_w2v = np.array(X_train_w2v)
X_test_w2v = np.array(X_test_w2v)

# 在使用神经网络前，对数据进行缩放
scl = preprocessing.StandardScaler()
X_train_w2v_scl = scl.fit_transform(X_train_w2v)
X_test_w2v_scl = scl.transform(X_test_w2v)

X_train_w2v_scl.shape[0]
X_train_w2v_scl.shape[1]

X_train_w2v_scl = X_train_w2v_scl.reshape(X_train_w2v_scl.shape[0],1,X_train_w2v_scl.shape[1])
X_test_w2v_scl = X_test_w2v_scl.reshape(X_test_w2v_scl.shape[0],1,X_test_w2v_scl.shape[1])

X_train_w2v_scl.shape[0]
X_train_w2v_scl.shape[1]
X_train_w2v_scl.shape[2]


y_train = np.array(y_train)
y_test = np.array(y_test)

# 对标签进行binarize处理
y_train_enc = np_utils.to_categorical(y_train)
y_test_enc = np_utils.to_categorical(y_test)


#建立一个多层 LSTM 模型
# 本例中一个长文本被转成了一行向量，所以time_step设置为1。
# 没一行向量有100个特征值，所以 feature = 100
time_step = 1
features = 100

model = Sequential()
model.add(LSTM(100,input_shape = (time_step,features) ,return_sequences=True,))
model.add(LSTM(40,return_sequences=True))
model.add(LSTM(25))
model.add(Dropout(0.3))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(80, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
model.summary()

history=model.fit(X_train_w2v_scl, y_train_enc, batch_size=128, epochs=100,validation_data=(X_test_w2v_scl, y_test_enc),verbose=1)

model.save('多层LSTM.h5') #保存

score = model.evaluate(X_test_w2v_scl, y_test_enc, batch_size=32)
print(score)

# 绘制准确率
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# 绘制损失
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

