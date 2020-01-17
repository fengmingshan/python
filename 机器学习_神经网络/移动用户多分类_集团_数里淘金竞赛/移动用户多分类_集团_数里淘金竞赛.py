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
# 数据清洗 & 空值填充 & 数据归一化 & str字段onehot编码
# =============================================================================

# 按照用户特征的大类来进行缺失值处理：
# 先处理 df_call，
df_call.isnull().any()
df_call.dtypes
# df_call 里没有发现缺失值 ,并且df_call 里面的特征都是数值型，不需要进行特殊处理 , pass
# df_call 直接进行 z-score 归一化
columns = [x for x in df_call.columns if x != 'user']
Standard_date = StandardScaler().fit_transform(df_call.drop('user',axis = 1))
df_Standard = pd.DataFrame(Standard_date,columns = columns)
df_call_Standard = pd.concat([df_call.user,df_Standard],axis = 1)

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
df_customer[df_customer.cust_access_net_dt <= 0] = int(df_customer[df_customer.cust_access_net_dt>0]['cust_access_net_dt'].mean())
df_customer[df_customer.birth_date <= 0] = int(df_customer[df_customer.birth_date>0]['birth_date'].mean())
# 归一化 和 onehot编码
# 有几个level属性以及 'gender' 属性 都是离散值，将它们都转成 onehot编码
level_feature = ['gender','credit_level' , 'membership_level' , 'star_level']
value_feature = [x for x in df_customer.columns if x not in level_feature and x != 'user']
df_customer_onehot = pd.get_dummies(df_customer[level_feature],columns=level_feature,sparse=False)
# 再进行z-score归一化
Standard_date = StandardScaler().fit_transform(df_customer[value_feature])
df_Standard = pd.DataFrame(Standard_date,columns = value_feature)
df_customer_Standard = pd.concat([df_call.user,df_customer_onehot,df_Standard],axis = 1)

# 处理 df_dpi ,
df_dpi.isnull().any()
df_dpi.dtypes
# df_dpi 里也没有发现缺失值，并且df_call 里面的特征都是数值型，不需要进行特殊处理 , pass
# df_dpi 直接进行 z-score 归一化
columns = [x for x in df_dpi.columns if x != 'user']
Standard_date = StandardScaler().fit_transform(df_dpi.drop('user',axis = 1))
df_Standard = pd.DataFrame(Standard_date,columns = columns)
df_dpi_Standard = pd.concat([df_call.user,df_Standard],axis = 1)

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
df_period.open_date[df_period.open_date <= 0] =  int(df_period[df_period.open_date>0]['open_date'].mean())
# 归一化 和 onehot编码
len(df_period.product_nbr.unique())
# df_period 的 'product_nbr' 用户产品编号 特征有98种取值不能进行onehot
# 所以这里通过神经网络的Embedding层对其进行降维度
# 输入数据是 402164 * 1，402164个样本，1个类别特征，且类别特征的可能值是0到97之间（98个）
# 对这1个特征做one-hot的话，应该为402164*98，
# embedding就是使原本应该one-hot的98维变为4维（也可以设为其他值）
# 这样输出结果应该是 402164*3
# 搭建模型
model = Sequential()
model.add(Embedding(98, 4, input_length=1)) # 我们把98个分类的数据降到4维
model.compile('rmsprop', 'mse')
# 处理输入数据
le = LabelEncoder()
le.fit(df_period.product_nbr.values.tolist())
input_array = le.transform(df_period.product_nbr.values.tolist())
output_array = model.predict(input_array)
product_nbr_dict = {}

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

#with open('用户数据_合.csv','w') as writer:
#    df.to_csv(writer,index =False)

#df = pd.read_csv('用户数据_合.csv', engine='python')

