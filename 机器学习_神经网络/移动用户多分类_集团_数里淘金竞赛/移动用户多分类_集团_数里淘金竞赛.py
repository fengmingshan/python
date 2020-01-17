# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:41:10 2019

@author: Administrator
"""
import pandas as pd
import numpy as np
import os
from dateutil.parser import parse
from datetime import date

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

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
df_terminal = pd.read_csv('./data/trmnl_data.csv', engine='python', encoding='utf-8')

# =============================================================================
# 数据清洗 & 空值填充 &
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

# df_call 直接进行
columns = [x for x in df_call.columns if x != 'user']
Standard_date = StandardScaler().fit_transform(df_call.drop('user', axis=1))
df_Standard = pd.DataFrame(Standard_date, columns=columns)
df_call_Standard = pd.concat([df_call.user, df_Standard], axis=1)

# df_customer归一化 和 onehot编码
# 有几个level属性以及 'gender' 属性 都是离散值，将它们都转成 onehot编码
level_feature = ['gender', 'credit_level', 'membership_level', 'star_level']
value_feature = [x for x in df_customer.columns if x not in level_feature and x != 'user']
df_customer_onehot = pd.get_dummies(df_customer[level_feature], columns=level_feature, sparse=False)
# 再进行z-score归一化
Standard_date = StandardScaler().fit_transform(df_customer[value_feature])
df_Standard = pd.DataFrame(Standard_date, columns=value_feature)
df_customer_Standard = pd.concat([df_call.user, df_customer_onehot, df_Standard], axis=1)

# df_dpi 直接进行 z-score 归一化
columns = [x for x in df_dpi.columns if x != 'user']
Standard_date = StandardScaler().fit_transform(df_dpi.drop('user', axis=1))
df_Standard = pd.DataFrame(Standard_date, columns=columns)
df_dpi_Standard = pd.concat([df_call.user, df_Standard], axis=1)

# df_period 归一化 和 分类特征降维
len(df_period.product_nbr.unique())
# df_period 的 'product_nbr' 用户产品编号 特征有98种取值不能进行onehot
# 所以这里通过神经网络的 Embedding层 对其进行降维度
# 输入数据是 402164 * 1，402164个样本，1个类别特征，且类别特征的可能值是0到97之间（98个）
# 对这1个特征做one-hot的话，应该为402164*98，
# embedding就是使原本应该one-hot的98维变为4维（也可以设为其他值）
# 这样输出结果应该是 402164*3
# 搭建模型
model = Sequential()
model.add(Embedding(98, 6, input_length=1))  # 我们把98个分类的数据降到4维
model.compile('rmsprop', 'mse')
# 处理输入数据
le = LabelEncoder()
le.fit(df_period.product_nbr.values.tolist())
input_array = le.transform(df_period.product_nbr.values.tolist())
output_array = model.predict(input_array)
output_array = output_array.reshape((402164,6))
df_product_nbr = pd.DataFrame(
    output_array,
    columns = [
        'product_nbr1',
        'product_nbr2',
        'product_nbr3',
        'product_nbr4',
        'product_nbr5',
        'product_nbr6'])
Standard_date = StandardScaler().fit_transform(df_period.open_date.values.reshape(-1,1))
Standard_date.shape
Standard_date = Standard_date.reshape(402164,)
df_Standard = pd.DataFrame(Standard_date, columns =['open_date'])
df_period_Standard = pd.concat([df_period.user, df_product_nbr,df_Standard,df_period.last_year_capture_user_flag], axis=1)

# df_terminal 归一化，分类特征降维
# 'pro_brand'厂家, 'term_model'型号，两个字段都是分类特征。
len(df_terminal.pro_brand.unique())
len(df_terminal.term_model.unique())
# 但是 'pro_brand'有185种, 'term_model'有2870种，如果进行onehot，会导致维度灾难。
# 所以我们还是用神经网络的 Embedding层 对其进行降维
# 搭建一个神经网络对 'pro_brand' 进行降维
model_185 = Sequential()
model_185.add(Embedding(185, 7, input_length=1))  # 我们把98个分类的数据降到4维
model_185.compile('rmsprop', 'mse')
le = LabelEncoder()
le.fit(df_terminal.pro_brand.values.tolist())
input_array = le.transform(df_terminal.pro_brand.values.tolist())
output_array = model_185.predict(input_array)
output_array = output_array.reshape((len(output_array),7))
df_pro_brand = pd.DataFrame(
    output_array,
    columns = [
        'pro_brand1',
        'pro_brand2',
        'pro_brand3',
        'pro_brand4',
        'pro_brand5',
        'pro_brand6',
        'pro_brand7'])
# 搭建一个神经网络对 'term_model' 进行降维
model_2870 = Sequential()
model_2870.add(Embedding(2870, 10, input_length=1))  # 我们把98个分类的数据降到4维
model_2870.compile('rmsprop', 'mse')
le = LabelEncoder()
le.fit(df_terminal.term_model.values.tolist())
input_array = le.transform(df_terminal.term_model.values.tolist())
output_array = model_2870.predict(input_array)
output_array = output_array.reshape((len(output_array),10))
df_term_model = pd.DataFrame(
    output_array,
    columns = [
        'term_model1',
        'term_model2',
        'term_model3',
        'term_model4',
        'term_model5',
        'term_model6',
        'term_model7',
        'term_model8',
        'term_model9',
        'term_model10'])


# with open('用户数据_合.csv','w') as writer:
#    df.to_csv(writer,index =False)

#df = pd.read_csv('用户数据_合.csv', engine='python')
