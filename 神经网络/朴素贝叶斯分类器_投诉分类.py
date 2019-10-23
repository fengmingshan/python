# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 10:57:16 2019

@author: Administrator
"""

import time
import string
import numpy as np
import os
import pandas as pd
import jieba

from sklearn import feature_extraction#导入特征抽取模块
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_curve
from sklearn import metrics

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

#文本向量化
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X_split)

type(X_vec)
X_vec.shape

#print(X_vec[1])
#print(X_vec[0].toarray())
#print(vectorizer.get_feature_names())
#print(vectorizer.vocabulary_)

X1=X_vec[:len(df1)]
X2=X_vec[len(df1):]

X_train, X_test, y_train, y_test = train_test_split(X1, df['标签'], test_size=0.15, random_state=0)
#print(X_train.shape,X_test.shape,y_train.shape,y_test.shape)
print(X_train[0])
def train_nbClassifier(X_train,y_train):
    from sklearn.naive_bayes import MultinomialNB # 导入朴素贝叶斯模型
    clf = MultinomialNB(alpha = 0.2)   #alpha为不确定性的权重，当学习集少的情况下，需要提高alpha来增加不确定性来拟合未知的数据，可以试试alpha=1的情况
    clf.fit(X_train,y_train)
    return clf

clf=train_nbClassifier(X_train,y_train)

y_pred=clf.predict(X_test)
y_pred[:10]

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

print('分类报告：',classification_report(y_test, y_pred))
print('全局准确率:',accuracy_score(y_test, y_pred))
print('混淆矩阵：',confusion_matrix(y_test, y_pred))

# 预测结果可视化
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

# 将分类报告输出为excel
def classifaction_report_csv(report):
    report_data = []
    lines = report.split('\n')
    for line in lines[2:-3]:
        row = {}
        row_data = line.split('      ')
        row['类别'] = row_data[1]
        row['精确率_precision'] = float(row_data[2])
        row['召回率_recall'] = float(row_data[3])
        row['f1_score'] = float(row_data[4])
        row['support'] = float(row_data[5])
        report_data.append(row)
    dataframe = pd.DataFrame.from_dict(report_data)
    return dataframe

report = classification_report(y_test, y_pred)
df_report = classifaction_report_csv(report)
if not os.path.exists('./结果可视化'):
    os.mkdir('./结果可视化')
with pd.ExcelWriter('./结果可视化/分类报告.xlsx') as writer:
    df_report.to_excel(writer,index = False)


confusion_mat = confusion_matrix(y_test, y_pred)

# 混淆矩阵可视化
import itertools
# 定义绘制混淆矩阵的函数
def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    Input
    - cm : 计算出的混淆矩阵的值
    - classes : 混淆矩阵中每一行每一列对应的列
    - normalize : True:显示百分比, False:显示个数
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    print(cm)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

classes = [2,4,5,6,8,11,14,15,16,19,21,23,28,31,32,33,36,37,42,43,44,45,46,47,49,50,52,53,54,56,57,59,60,64,66,67,69,72,74,77,79]

plt.figure(figsize=(30, 25))
plot_confusion_matrix(confusion_mat, classes=classes, normalize=True, title='混淆矩阵')
plt.show()
plt.savefig("./结果可视化/混淆矩阵3.png",format='png', dpi=500)
