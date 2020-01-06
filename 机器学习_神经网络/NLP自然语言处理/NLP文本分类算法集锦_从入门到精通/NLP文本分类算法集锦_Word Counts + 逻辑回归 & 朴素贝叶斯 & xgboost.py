# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 19:35:28 2020

@author: Administrator
"""
import pandas as pd
import numpy as np
import os

from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

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

def multiclass_logloss(actual, predicted, eps=1e-15):
    """对数损失度量（Logarithmic Loss  Metric）的多分类版本。
    :param actual: 包含actual target classes的数组
    :param predicted: 分类预测结果矩阵, 每个类别都有一个概率
    """
    # 如果 actual还不是二进制数组，则需要先将actual转为二进制数组
    if len(actual.shape) == 1:
        actual2 = np.zeros((actual.shape[0], predicted.shape[1]))
        for i, val in enumerate(actual):
            actual2[i, val] = 1
        actual = actual2

    clip = np.clip(predicted, eps, 1 - eps)
    rows = actual.shape[0]
    vsota = np.sum(actual * np.log(clip))
    return -1.0 / rows * vsota

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

stwlist=[line.strip() for line in open('./停用词表.txt',
'r',encoding='utf-8').readlines()]

# scikit-learn中的CountVectorizer进行 Word Counts
ctv = CountVectorizer(min_df=3,
                      max_df=0.5,
                      ngram_range=(1,2),
                      stop_words = stwlist)

# 使用Count Vectorizer来fit训练集和测试集（半监督学习）
ctv.fit(list(x_train) + list(x_test))
x_train_ctv =  ctv.transform(x_train)
x_test_ctv = ctv.transform(x_test)

#基于word counts特征来fit一个简单的逻辑回归
clf = LogisticRegression(C=1.0,solver='lbfgs',multi_class='multinomial')
clf.fit(x_train_ctv, y_train)
predictions = clf.predict_proba(x_test_ctv)

print ("logloss: %0.3f " % multiclass_logloss(y_test, predictions))

#基于word counts特征来fit朴素贝叶斯
clf = MultinomialNB()
clf.fit(x_train_ctv, y_train)
predictions = clf.predict_proba(x_test_ctv)
print ("logloss: %0.3f " % multiclass_logloss(y_test, predictions))

# 基于word counts特征，使用xgboost
clf = xgb.XGBClassifier(max_depth=7, n_estimators=200, colsample_bytree=0.8,
                        subsample=0.8, nthread=10, learning_rate=0.1)
clf.fit(x_train_ctv.tocsc(), y_train)
predictions = clf.predict_proba(x_test_ctv.tocsc())

print ("logloss: %0.3f " % multiclass_logloss(y_test, predictions))

