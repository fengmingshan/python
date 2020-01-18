# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:41:10 2019

@author: Administrator
"""
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from dateutil.parser import parse
from datetime import date

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # 随机森林
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from keras.layers.embeddings import Embedding
from keras.models import Sequential

work_path = 'D:/Notebook/2019年12月_集团数里淘金竞赛_移动用户多分类'
os.chdir(work_path)

file_list = os.listdir('.')

# 读取数据
df_call = pd.read_csv('./data/call_data.csv', engine='python', encoding='utf-8')
df_customer = pd.read_csv('./data/cust_data.csv', engine='python', encoding='utf-8')
df_dpi = pd.read_csv('./data/dpi_data.csv', engine='python', encoding='utf-8')
df_period = pd.read_csv('./data/prd_data.csv', engine='python', encoding='utf-8')
df_terminal = pd.read_csv('./data/trmnl_data_update.csv', engine='python', encoding='utf-8')

# =============================================================================
# 数据清洗 & 空值填充
# =============================================================================

# 按照用户特征的大类来进行缺失值处理：
# 先处理 df_call，
df_call.isnull().any()
df_call.dtypes
# df_call 里没有缺失值 ,且df_call 里面的特征都是数值型，不需要进行特殊处理 , pass

# 处理 df_customer
# 获取 df_customer 表中所有的特征字段
customer_feature = df_customer.drop('user', axis=1).columns
# 统计某一列缺失值的数量
df_customer.cust_access_net_dt.isnull().value_counts()
# 用户个人信息共有8个字段,其中有950条记录是全部特征都缺失，
# 对 df_customer中的所有缺失的特征值进行填充，采用众数填充
for col in customer_feature:
    df_customer[col].fillna(df_customer[col].mode()[0], inplace=True)
# df_customer 中有两个特征cust_access_net_dt 用户入网日期 和 birth_date 用户生日
# 都被转成了数值，这里必须手动将它转回来，都转成时长，单位是天
today = date.today().strftime('%Y%m%d')
df_customer.cust_access_net_dt = df_customer.cust_access_net_dt.map(lambda x: str(x)[:8])
df_customer.cust_access_net_dt = df_customer.cust_access_net_dt.map(
    lambda x: (parse(today) - parse(x)).days)
df_customer.birth_date = df_customer.birth_date.map(lambda x: str(x)[:8])
df_customer.birth_date = df_customer.birth_date.map(lambda x: (parse(today) - parse(x)).days)
(df_customer.cust_access_net_dt >= 0).value_counts()
(df_customer.birth_date >= 0).value_counts()
# 处理完之后 'cust_access_net_dt' ， 'birth_date'两个字段还有小雨零的值
df_customer[df_customer.cust_access_net_dt <= 0] = int(
    df_customer[df_customer.cust_access_net_dt > 0]['cust_access_net_dt'].mean())
df_customer[df_customer.birth_date <= 0] = int(
    df_customer[df_customer.birth_date > 0]['birth_date'].mean())

# 处理 df_dpi ,
df_dpi.isnull().any()
df_dpi.dtypes
# df_dpi 里也没有缺失值，并且df_call 里面的特征都是数值型，不需要进行特殊处理 , pass

# 处理 df_period
df_period.isnull().any()
df_period.open_date.isnull().value_counts()
# 'open_date' 字段有缺失值，缺失了5行,使用众数来填充
df_period.open_date.fillna(df_period.open_date.mode()[0], inplace=True)
# 'open_date' 字段也是一个日期字段，但是被转成了数值型，需要手动转成时长，单位为天
df_period.open_date = df_period.open_date.map(lambda x: str(x)[:8])
df_period.open_date = df_period.open_date.map(lambda x: (parse(today) - parse(x)).days)
(df_period.open_date <= 0).value_counts()
# 处理完之后 'open_date' 字段还有小雨零的值
df_period.open_date[df_period.open_date <= 0] = int(
    df_period[df_period.open_date > 0]['open_date'].mean())

# 接着处理 df_terminal
df_terminal.isnull().any()
# df_terminal 里也没有发现缺失值
# 'register_date' 字段是一个日期字段 ，但是被转成了数值型，需要手动转成时长，单位为天
df_terminal.register_date = df_terminal.register_date.map(lambda x: (parse(today) - parse(x)).days)

# 合并所有表格
df = pd.merge(df_call, df_customer, how='left', on='user')
df = pd.merge(df, df_dpi, how='left', on='user')
df = pd.merge(df, df_period, how='left', on='user')
df = pd.merge(df, df_terminal, how='left', on='user')

df.isnull().any()
# 查看有多少行存在缺失值
df_null = df[df.isnull().values].drop_duplicates()
len(df_null)
# 有84394行存在缺失值，所以必须要进行缺失值填充，不能简单的删除有缺失值的行
# 查看每个特征分别缺失了多少条记录
df_null.isnull().sum()
# 筛选出所有的有缺失值的特征名
df_feature = df.isnull().any()
df_null_feature = df_feature[df_feature]
null_feature = list(df_null_feature.index)
for feature in null_feature:
    df[feature].fillna(df[feature].mode()[0], inplace=True)
# 再次检查缺失值
df.isnull().any()
# 这次所有字段都没有缺失了，可以进行下一步

# =============================================================================
# 数据归一化 & 分类特征onehot编码
# =============================================================================

# 数值型的特征全部一起进行  z-score 归一化
num_feature = []
# 按df_call 、 df_customer 、 df_dpi 、 df_period 、 df_terminal 找出数值特征。
num_feature.extend(list(df_call.drop('user', axis=1).columns))
num_feature.extend(list(df_customer.drop(
    ['user', 'credit_level', 'membership_level', 'gender', 'star_level'], axis=1).columns))
num_feature.extend(list(df_dpi.drop('user', axis=1).columns))
num_feature.extend(list(df_period.drop(['user', 'product_nbr'], axis=1).columns))
num_feature.extend(list(df_terminal.drop(['user', 'pro_brand', 'term_model'], axis=1).columns))

Standard_date = StandardScaler().fit_transform(df[num_feature])
df_Standard = pd.DataFrame(Standard_date, columns=num_feature)
for col in num_feature:
    df[col] = df_Standard[col]

# =============================================================================
# 维度较少的特征（ <= 4），进行onehot编码
# =============================================================================
df.credit_level.unique()  # 7个种类
df.membership_level.unique()  # 4个种类
df.gender.unique()  # 3个种类
df.star_level.unique()  # 10个种类

fewer_kind_feature = []
fewer_kind_feature.append('membership_level')
fewer_kind_feature.append('gender')

df_onehot = pd.get_dummies(df, columns=fewer_kind_feature, sparse=False)

# =============================================================================
# 维度较多的分类特征，用 Embedding层 进行降维
# =============================================================================
len(df.credit_level.unique())  # 7类
len(df.star_level.unique())  # 10类
len(df.product_nbr.unique())  # 98类
len(df.pro_brand.unique())  # 185类
len(df.term_model.unique())  # 2870类

major_kind_feature = []
major_kind_feature.append('credit_level')
major_kind_feature.append('star_level')
major_kind_feature.append('product_nbr')
major_kind_feature.append('pro_brand')
major_kind_feature.append('term_model')

# 降维 'credit_level' 信用等级，特征有7种取值不建议进行onehot
model_7 = Sequential()
model_7.add(Embedding(7, 2, input_length=1))  # 我们把7个分类的数据降到2维
model_7.compile('rmsprop', 'mse')
le = LabelEncoder()
le.fit(df.credit_level.values.tolist())
input_array = le.transform(df.credit_level.values.tolist())
output_array = model_7.predict(input_array)
output_array = output_array.reshape((402164, 2))
df_credit_level = pd.DataFrame(
    output_array,
    columns=[
        'credit_level1',
        'credit_level2'])

# 降维 'star_level' 用户星级，特征有10种取值不建议进行onehot
model_10 = Sequential()
model_10.add(Embedding(10, 2, input_length=1))  # 我们把7个分类的数据降到2维
model_10.compile('rmsprop', 'mse')
le = LabelEncoder()
le.fit(df.star_level.values.tolist())
input_array = le.transform(df.star_level.values.tolist())
output_array = model_10.predict(input_array)
output_array = output_array.reshape((402164, 2))
df_star_level = pd.DataFrame(
    output_array,
    columns=[
        'star_level1',
        'star_level2'])

# 降维 'product_nbr' 用户产品编号 特征有98种取值不能进行onehot
# 所以这里通过神经网络的 Embedding层 对其进行降维度
# 输入数据是 402164 * 1，402164个样本，1个类别特征，且类别特征的可能值是0到97之间（98个）
# 对这1个特征做one-hot的话，应该为402164*98，
# embedding就是使原本应该one-hot的98维变为4维（也可以设为其他值）
# 这样输出结果应该是 402164*3
# 搭建模型
model_98 = Sequential()
model_98.add(Embedding(98, 5, input_length=1))  # 我们把98个分类的数据降到4维
model_98.compile('rmsprop', 'mse')
# 处理输入数据
le = LabelEncoder()
le.fit(df.product_nbr.values.tolist())
input_array = le.transform(df.product_nbr.values.tolist())
output_array = model_98.predict(input_array)
output_array = output_array.reshape((402164, 5))
df_product_nbr = pd.DataFrame(
    output_array,
    columns=[
        'product_nbr1',
        'product_nbr2',
        'product_nbr3',
        'product_nbr4',
        'product_nbr5'])

# df_terminal 的 'pro_brand'厂家, 'term_model'型号，两个字段都是分类特征。
len(df.pro_brand.unique())
len(df.term_model.unique())
# 但是 'pro_brand'有185种, 'term_model'有2870种，如果进行onehot，会导致维度灾难。
# 所以我们还是用神经网络的 Embedding层 对其进行降维
# 搭建一个神经网络对 'pro_brand' 进行降维
model_185 = Sequential()
model_185.add(Embedding(185, 6, input_length=1))  # 我们把98个分类的数据降到4维
model_185.compile('rmsprop', 'mse')
le = LabelEncoder()
le.fit(df.pro_brand.values.tolist())
input_array = le.transform(df.pro_brand.values.tolist())
output_array = model_185.predict(input_array)
output_array = output_array.reshape((len(output_array), 6))
df_pro_brand = pd.DataFrame(
    output_array,
    columns=[
        'pro_brand1',
        'pro_brand2',
        'pro_brand3',
        'pro_brand4',
        'pro_brand5',
        'pro_brand6'])

# 搭建一个神经网络对 'term_model' 进行降维
model_2870 = Sequential()
model_2870.add(Embedding(2870, 9, input_length=1))  # 我们把98个分类的数据降到4维
model_2870.compile('rmsprop', 'mse')
le = LabelEncoder()
le.fit(df.term_model.values.tolist())
input_array = le.transform(df.term_model.values.tolist())
output_array = model_2870.predict(input_array)
output_array = output_array.reshape((len(output_array), 9))
df_term_model = pd.DataFrame(
    output_array,
    columns=[
        'term_model1',
        'term_model2',
        'term_model3',
        'term_model4',
        'term_model5',
        'term_model6',
        'term_model7',
        'term_model8',
        'term_model9'])

df_onehot.drop(major_kind_feature, axis=1, inplace=True)
df_result = pd.concat([df_onehot, df_credit_level, df_star_level,
                       df_product_nbr, df_pro_brand, df_term_model], axis=1)

df_label = pd.read_csv('./data/train_result.csv', engine='python', encoding='utf-8')

label_list = sorted(df_label.label.unique())
label2num_dict = {k: v for v, k in enumerate(label_list)}
num2label_dict = {k: v for k, v in enumerate(label_list)}
df_label.label = df_label.label.map(label2num_dict)
df_label.label.astype(int,inplace = True)

df_result = pd.merge(df_result, df_label, how='left', on='user')

df_train = df_result[~df_result.label.isnull()]
df_train.label = df_train.label.astype(int,inplace = True)
df_train.reset_index(drop = True ,inplace = True)

df_test = df_result[df_result.label.isnull()]
df_test.drop('label' ,axis = 1 ,inplace = True)
df_test.reset_index(drop = True ,inplace = True)

with open('./训练集.csv','w') as writer:
    df_train.to_csv(writer,index =False)

with open('./测试集.csv','w') as writer:
    df_test.to_csv(writer,index =False)

with open('./全部数据_完成预处理.csv','w') as writer:
    df_result.to_csv(writer,index =False)

# =============================================================================
# 拆分 训练集 和 测试集
# =============================================================================
X = df_train.drop(['user', 'label'], axis=1)
y = df_train.label.values
X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.3, stratify=y, shuffle=True, random_state=42)
X_train.shape
y_train.shape
X_valid.shape
y_valid.shape

# =============================================================================
# 建模训练
# =============================================================================
rf = RandomForestClassifier(random_state=420)
rf.fit(X_train, y_train)  # 训练模型

y_pred = rf.predict(X_valid)

Accuracy = accuracy_score(y_valid ,y_pred, normalize =True  )
Recall = recall_score(y_valid, y_pred, average='macro')
F1 = f1_score(y_valid, y_pred, average='weighted')
#F1_score = 2 * accuracy_score * recall_acc / (accuracy_score + recall_score)
F1_2 = F1**2
print('准确率 = {0} %'.format(round(Accuracy, 2)))
print('召回率 = {0} %'.format(round(Recall * 100, 2)))
print('F1 = {0}'.format(F1))
print('(F1)2 = {0}'.format(F1_2))


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

rf_matrix = confusion_matrix(y_valid, y_pred)
# 绘制混淆矩阵
class_names = [0, 1, 2, 3, 4]
plt.figure()
plot_confusion_matrix(rf_matrix,
                      classes=class_names,
                      normalize=False,
                      title='Confusion matrix')
plt.show()

# 读入测试集，测试模型
X_test = df_test.drop('user' ,axis = 1)

y_test = rf.predict(X_test)

df_pred = pd.DataFrame({'label' : y_test})
df_pred = df_pred.label.map(num2label_dict)

# 合成上报文件
df_res = pd.concat([df_test.user,df_pred] ,axis = 1)
df_res['num'] = df_res.user.map(lambda x:int(x.split('_')[1]))
df_res.sort_values(by='num', ascending=True, inplace=True)
df_res.reset_index(drop = True ,inplace = True)
with open('./submission.csv','w') as writer:
    df_res.to_csv(writer ,index =False)
