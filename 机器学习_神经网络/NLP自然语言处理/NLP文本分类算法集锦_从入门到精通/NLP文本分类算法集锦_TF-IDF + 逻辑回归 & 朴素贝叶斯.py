# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 09:55:04 2020

@author: Administrator
"""
#载入接下来分析用的库
import pandas as pd
import numpy as np
import os
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
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

# 将数字映射成一个占位符的函数
def number_normalizer(tokens):
    """ 将所有数字标记映射为一个占位符（Placeholder）。
    对于许多实际应用场景来说，以数字开头的tokens不是很有用，
    但这样tokens的存在也有一定相关性。 通过将所有数字都表示成同一个符号，可以达到降维的目的。
    """
    return ("#NUMBER" if token[0].isdigit() else token for token in tokens)

class NumberNormalizingVectorizer(TfidfVectorizer):
    def build_tokenizer(self):
        tokenize = super(NumberNormalizingVectorizer, self).build_tokenizer()
        return lambda doc: list(number_normalizer(tokenize(doc)))

stwlist=[line.strip() for line in open('./停用词表.txt',
'r',encoding='utf-8').readlines()]

tfv = NumberNormalizingVectorizer(min_df=3,
                                  max_df=0.5,
                                  max_features=None,
                                  ngram_range=(1, 2),
                                  use_idf=True,
                                  smooth_idf=True,
                                  stop_words = stwlist)

# 使用TF-IDF来fit训练集和测试集（半监督学习）
tfv.fit(list(x_train) + list(x_test))
x_train_tfv =  tfv.transform(x_train)
x_test_tfv = tfv.transform(x_test)

#利用提取的TFIDF特征来fit一个简单的Logistic Regression
clf = LogisticRegression(C=1.0,solver='lbfgs',multi_class='multinomial')
clf.fit(x_train_tfv, y_train)
predictions = clf.predict_proba(x_test_tfv)

# 输出loss
print ("logloss: %0.3f " % multiclass_logloss(y_test, predictions))

# 将预测结果20维的向量转成分类
y_pred = []
for item in predictions:
    y_pred.append(list(item).index(max(item)))
y_pred[:10]
# 输出分类报告
print(classification_report(y_pred, y_test))

# 绘制分类报告
labels = list(range(0,20))
maxtrix = confusion_matrix(y_test, y_pred,labels=labels)
plt.matshow(maxtrix,cmap=plt.cm.Blues_r)
plt.colorbar()
plt.xlabel('Pred')
plt.ylabel('True')
plt.xticks(np.arange(maxtrix.shape[1]),labels)
plt.yticks(np.arange(maxtrix.shape[1]),labels)

# 全局准确率
print('全局准确率:%.2f%%' % (accuracy_score(y_test, y_pred)*100))


#利用提取的TFIDF特征来fit朴素贝叶斯
clf = MultinomialNB()
clf.fit(x_train_tfv, y_train)
predictions = clf.predict_proba(x_test_tfv)

print ("logloss: %0.3f " % multiclass_logloss(y_test, predictions))