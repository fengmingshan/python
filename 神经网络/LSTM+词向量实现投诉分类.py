# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:28:25 2019

@author: Administrator
"""

#载入接下来分析用的库
import pandas as pd
import numpy as np
import os
import jieba
import xgboost as xgb
from tqdm import tqdm
from sklearn.svm import SVC
from keras.models import Sequential
from keras.layers.recurrent import LSTM, GRU
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.embeddings import Embedding
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from keras.layers import GlobalMaxPooling1D, Conv1D, MaxPooling1D, Flatten, Bidirectional, SpatialDropout1D
from keras.preprocessing import sequence, text
from keras.callbacks import EarlyStopping
from nltk import word_tokenize

# 定义损失评估函数
def multiclass_logloss(actual, predicted, eps=1e-15):
    """对数损失度量（Logarithmic Loss  Metric）的多分类版本。
    :param actual: 包含actual target classes的数组
    :param predicted: 分类预测结果矩阵, 每个类别都有一个概率
    """
    # Convert 'actual' to a binary array if it's not already:
    if len(actual.shape) == 1:
        actual2 = np.zeros((actual.shape[0], predicted.shape[1]))
        for i, val in enumerate(actual):
            actual2[i, val] = 1
        actual = actual2

    clip = np.clip(predicted, eps, 1 - eps)
    rows = actual.shape[0]
    vsota = np.sum(actual * np.log(clip))
    return -1.0 / rows * vsota


data_path = 'D:/Notebook/通过机器学习进行投诉分类'
os.chdir(data_path)

df1=pd.read_excel('train-test-ts-V2.xls', sheetname='训练集1') # 数据类型：DataFrame
df2=pd.read_excel('train-test-ts-V2.xls', sheetname='测试集1') # 数据类型：DataFrame
df=df1.append(df2) #把两个DataFrame拼接起来，方便进行数据预处理
df.head(5)
df.columns
df.loc[0,'文本']
print(len(df))
print(len(df1))
print(len(df2))

# 去除文本中的一些网页格式
df['文本'] = df['文本'].map(lambda x:x.replace('①',''))
df['文本'] = df['文本'].map(lambda x:x.replace('②',''))
df['文本'] = df['文本'].map(lambda x:x.replace('③',''))
df['文本'] = df['文本'].map(lambda x:x.replace('④',''))
df['文本'] = df['文本'].map(lambda x:x.replace('⑤',''))
df['文本'] = df['文本'].map(lambda x:x.replace('【',''))
df['文本'] = df['文本'].map(lambda x:x.replace('】',''))
df['文本'] = df['文本'].map(lambda x:x.replace('(',''))
df['文本'] = df['文本'].map(lambda x:x.replace(')',''))
df['文本'] = df['文本'].map(lambda x:x.replace(':',''))
df['文本'] = df['文本'].map(lambda x:x.replace('<br>',''))
df['文本'] = df['文本'].map(lambda x:x.replace('<b>',''))
df['文本'] = df['文本'].map(lambda x:x.replace('</b>',''))
df['文本'] = df['文本'].map(lambda x:x.replace('\n',''))
df['文本'] = df['文本'].map(lambda x:x.replace('-',''))
df['文本'] = df['文本'].map(lambda x:x.replace('>',''))
df['文本'] = df['文本'].map(lambda x:x.replace('：',''))
df['文本'] = df['文本'].map(lambda x:x.replace('；',''))
df['文本'] = df['文本'].map(lambda x:x.replace('.',''))
df['文本'] = df['文本'].map(lambda x:x.replace('（',''))
df['文本'] = df['文本'].map(lambda x:x.replace('）',''))
df['文本'] = df['文本'].map(lambda x:x.replace('，',''))
df['文本'] = df['文本'].map(lambda x:x.replace('。',''))
df['文本'] = df['文本'].map(lambda x:x.replace('、',''))

# 去除文本中的数字串
def replace_num(text):
    import re
    p1 = r"[0-9]+" # 这是我们写的正则表达式规则，你现在可以不理解啥意思
    pattern1 = re.compile(p1) # 我们在编译这段正则表达式
    res = pattern1.findall(text)
    res.sort(key = lambda i:len(i),reverse=True)
    if len(res) > 0: # 如果匹配成功
        for i in range(len(res)):
            new_text = text.replace(res[i],'') # 打印出来
            text = new_text
    return  text

df['文本'] = df['文本'].map(lambda x:replace_num(x))


#定义停词函数
def loadStopWords():
    stop = []
    for line in open('stopWord.txt').readlines():
        stop.append(line)
    return list(set(stop))

#定义切词函数
def cutWords(msgs,stopWords):
    arr_leftWords=[]
    for msg in msgs:
        seg_list = jieba.cut(msg,cut_all=False)
        #key_list = jieba.analyse.extract_tags(msg,20) #get keywords
        #leftWords = []
        leftWords=''
        for i in seg_list:#for i in y,y可以是列表、元组、字典、Series
            if (i not in stopWords):
                leftWords+=' '+i
        leftWords.strip()
        arr_leftWords.append(leftWords)
    return arr_leftWords

X=df['文本']
X[:5]

# 读取停用词表
stopwords = loadStopWords()
print(len(stopwords))
stopwords[:20]

# 对文本 X 进行分词操作
X_split = cutWords(X,stopwords)

X_train, X_test, y_train, y_test = train_test_split(X_split, df['标签'], test_size=0.15, random_state=0)
#print(X_train.shape,X_test.shape,y_train.shape,y_test.shape)

# =============================================================================
# 训练word2vec词向量:
# =============================================================================
import gensim
model = gensim.models.Word2Vec(X_split,min_count =5,window =8,size=100)   # X_split是经分词后的文本构成的list，也就是tokens的列表的列表
embeddings_index = dict(zip(model.wv.index2word, model.wv.vectors))
print('Found %s word vectors.' % len(embeddings_index))

def sent2vec(s):
    words = str(s)
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

# 对训练集和验证集使用上述函数，进行文本向量化处理
X_train_w2v = [sent2vec(x) for x in tqdm(X_train)]
X_test_w2v = [sent2vec(x) for x in tqdm(X_test)]

X_train_w2v = np.array(X_train_w2v)
X_test_w2v = np.array(X_test_w2v)

# 在使用神经网络前，对数据进行缩放
scl = preprocessing.StandardScaler()
X_train_w2v_scl = scl.fit_transform(X_train_w2v)
X_test_w2v_scl = scl.transform(X_test_w2v)

# 对标签进行binarize处理，变成one-hot的形式
#y_train_enc = np_utils.to_categorical(y_train)
#y_test_enc = np_utils.to_categorical(y_test)


# 使用 keras tokenizer
token = text.Tokenizer(num_words=None)
max_len = 70

token.fit_on_texts(list(X_train) + list(X_test))
xtrain_seq = token.texts_to_sequences(X_train)
xvalid_seq = token.texts_to_sequences(X_test)

#对文本序列进行zero填充
xtrain_pad = sequence.pad_sequences(xtrain_seq, maxlen=max_len)
xvalid_pad = sequence.pad_sequences(xvalid_seq, maxlen=max_len)

word_index = token.word_index


#基于已有的数据集中的词汇创建一个词嵌入矩阵（Embedding Matrix）
embedding_matrix = np.zeros((len(word_index) + 1, 100))
for word, i in tqdm(word_index.items()):
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

# 基于前面训练的Word2vec词向量，使用1个两层的LSTM模型
model = Sequential()
model.add(Embedding(len(word_index) + 1,
                     100,
                     weights=[embedding_matrix],
                     input_length=max_len,
                     trainable=False))
model.add(SpatialDropout1D(0.3))
model.add(LSTM(100, dropout=0.3, recurrent_dropout=0.3))

model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.8))

model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.8))

model.add(Dense(80,activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')

model.summary()

model.fit(xtrain_pad, y = y_train, batch_size=512, epochs=10, verbose=1, validation_data=(xvalid_pad, y_test))

model.save('lstm_model_10epochs.h5')