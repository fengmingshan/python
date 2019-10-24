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
w2vModel = gensim.models.Word2Vec(X_words_list, min_count=5, window=8, size=100)
embeddings_dict = dict(zip(w2vModel.wv.index2word, w2vModel.wv.vectors))
print('共训练 %s 个词向量.' % len(embeddings_dict))
w2vModel.save('w2vModel.model')

# 加载自己以前训练的词向量
#w2vModel = gensim.models.Word2Vec.load('w2vModel.model')
#embeddings_dict = dict(zip(w2vModel.wv.index2word, w2vModel.wv.vectors))

# 使用 keras Tokenizer对词组进行编码
# 创建了一个Tokenizer对象后，使用该对象的fit_on_texts()函数，以空格去识别每个词
# 输入的文本中的每个词编号，编号是根据词频的，词频越大，编号越小。
token = text.Tokenizer(num_words=None)
max_len = 70

token.fit_on_texts(list(X_train) + list(X_test))
xtrain_seq = token.texts_to_sequences(X_train)
xvalid_seq = token.texts_to_sequences(X_test)

# 对文本序列进行zero填充,因为有的文本不足70个词
xtrain_pad = sequence.pad_sequences(xtrain_seq, maxlen = max_len)
xvalid_pad = sequence.pad_sequences(xvalid_seq, maxlen = max_len)

word_index = token.word_index


# 基于已有的数据集中的词汇创建一个词嵌入矩阵（Embedding Matrix），需要参与神经网络模型训练
embedding_matrix = np.zeros((len(word_index) + 1, 100))
for word, i in tqdm(word_index.items()):
    embedding_vector =  embeddings_dict1.get(word)
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

model.add(Dense(80, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')

model.summary()

model.fit(
    xtrain_pad,
    y=y_train,
    batch_size=512,
    epochs=3,
    verbose=1,
    validation_data=(
        xvalid_pad,
        y_test))

model.save('lstm_model_1_epochs.h5')


# =============================================================================
# 模型评估
# =============================================================================
# 预测结果可视化
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


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


y_pred = model.predict(xvalid_pad, verbose=0)
y_pred[0]

# 将预测结果80维的向量转成分类
y_pred_list = []
for item in y_pred:
    y_pred_list.append(list(item).index(max(item)))

report = classification_report(y_test, y_pred_list)
df_report = classifaction_report_csv(report)

if not os.path.exists('./结果可视化'):
    os.mkdir('./结果可视化')
with pd.ExcelWriter('./结果可视化/LSTM分类报告.xlsx') as writer:
    df_report.to_excel(writer, index=False)

# 混淆矩阵可视化
# 定义绘制混淆矩阵的函数


def plot_confusion_matrix(
        cm,
        classes,
        normalize=False,
        title='Confusion matrix',
        cmap=plt.cm.Blues):
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


# 混淆矩阵绘图
confusion_mat = confusion_matrix(y_test, y_pred_list)

classes = [
    1,
    2,
    4,
    5,
    6,
    8,
    11,
    12,
    14,
    15,
    16,
    19,
    20,
    21,
    23,
    24,
    26,
    31,
    33,
    34,
    36,
    37,
    38,
    39,
    42,
    43,
    44,
    45,
    47,
    50,
    51,
    52,
    53,
    54,
    56,
    57,
    58,
    59,
    60,
    67,
    69,
    71,
    72,
    74,
    77,
    79]

plt.figure(figsize=(30, 25))
plot_confusion_matrix(confusion_mat, classes=classes, normalize=True, title='混淆矩阵')
plt.show()
plt.savefig("./结果可视化/混淆矩阵_.png", format='png', dpi=500)

# 全局准确率
print('全局准确率:', accuracy_score(y_test, y_pred_list))

# =============================================================================
# 加载模型
# =============================================================================
data_path = 'D:/Notebook/通过机器学习进行投诉分类'
os.chdir(data_path)

# 读取模型
model = load_model('lstm_model_10epochs.h5')
# 预测
y_pred = model.predict(xvalid_pad, verbose=0)
print(y_pred[0])

# 将预测结果80维的向量转成分类
y_pred_list = []
for item in y_pred:
    y_pred_list.append(list(item).index(max(item)))
