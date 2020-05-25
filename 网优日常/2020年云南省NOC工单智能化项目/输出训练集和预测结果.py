import pandas as pd
import os
from sklearn.model_selection import train_test_split
import jieba
from sklearn.externals import joblib
from keras.models import load_model
from keras.preprocessing import sequence
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

data_path = r'D:\2020年工作\2020年NOC工单智能化项目'
os.chdir(data_path)
df=pd.read_excel('./训练集/训练集_合_6000.xlsx') #数据类型：DataFrame

df['分类'] = ''
df['分类'][df['规范分类']=='规范'] = '规范'
df['分类'][df['规范分类']!='规范'] = '不规范'

# 去除提请销障内容中的一些网页格式
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('①',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('②',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('③',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('④',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('⑤',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('【',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('】',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('(',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace(')',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace(':',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('<br>',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('<b>',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('</b>',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('\n',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('-',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('>',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('：',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('；',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace(';',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('.',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('（',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('）',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('，',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('。',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('、',''))
df['提请销障内容'] = df['提请销障内容'].map(lambda x:x.replace('/',''))

#定义读取停词表的函数
def loadStopWords():
    stop = []
    for line in open('./stopWord.txt').readlines():
        stop.append(line)
    return list(set(stop))


def cutWords(msgs,stopWords):
    jieba.load_userdict("userdict.txt")
    arr_leftWords=[]
    for msg in msgs:
        seg_list = jieba.cut(msg,cut_all=False)
        leftWords=''
        for i in seg_list:#for i in y,y可以是列表、元组、字典、Series
            if (i not in stopWords):
                leftWords+=' '+i
        leftWords.strip()
        arr_leftWords.append(leftWords)
    return arr_leftWords

stopwords=loadStopWords()
X=df['提请销障内容']

# 将标签转为数字
label_list = sorted(df['分类'].unique().tolist())

# 构造 标签转数字的字典
label2num_dict = {v:k for k , v in enumerate(label_list)}

# 构造 数字转标签的字典
num2label_dict = {k:v for k , v in enumerate(label_list)}

# 将分类标签转换成数字
df['label']= df['分类'].map(label2num_dict)

# 拆分表格待以后使用
# 拆分训练集和测试集
X_train, X_test_original, y_train, y_test = train_test_split(df, df.label, test_size=0.3, stratify=df.label, shuffle=True, random_state=41)

X=df['提请销障内容']
X_cut = cutWords(X,stopwords) #X数据类型为list

# 拆分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_cut, df.label, test_size=0.3, stratify=df.label, shuffle=True, random_state=41)
X_test_original['分词'] = X_test

X_test_original = X_test_original[['提请销障内容','分词', '专业', '选择的一级定位', '选择的二级定位', '规范分类', '分类', 'label']]

# 加载自己以前训练的词向量
import gensim
w2vModel = gensim.models.Word2Vec.load('./w2vModel.model')
embeddings_dict = dict(zip(w2vModel.wv.index2word, w2vModel.wv.vectors))

# 载入tokenizer模型用来统计词频
token = joblib.load('./token_file.pkl')
word_index = token.word_index

model = load_model('./lstm_model_15_epochs_nosample.h5')
xtest_seq = token.texts_to_sequences(X_test) #
max_len = 216
xtest_pad = sequence.pad_sequences(xtest_seq, maxlen=max_len)

y_pred_prob = model.predict(xtest_pad, verbose=0)
y_pred_list = []
for item in y_pred_prob:
    y_pred_list.append(list(item).index(max(item)))


import itertools
# 定义绘制混淆矩阵的函数
def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
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

# 全局准确率
print('全局准确率:',accuracy_score(y_test, y_pred_list))

X_test_original['预测值'] = y_pred_list
with open('./测试集.csv','w',newline = '') as f:
    X_test_original.to_csv(f,index =False)

