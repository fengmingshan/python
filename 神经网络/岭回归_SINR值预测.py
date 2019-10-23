# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:28:13 2019

@author: Administrator
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import *

from tensorflow import keras
from tensorflow.keras.layers import *

%matplotlib inline

data_path = 'D:/Notebook/通过MR数据预测采样点SINR值'
os.chdir(data_path)

df = pd.read_csv('曲靖DT数据_总.csv', engine='python')
df.head(5)
df.describe()
df.dtypes
df.columns

# 观察预测值SINR的概率分布
sns.distplot(df.SINR)


df['Neighbor_COUNT'] = df[['Neighbor1_RSRP',
                           'Neighbor2_RSRP',
                           'Neighbor3_RSRP',
                           'Neighbor4_RSRP',
                           'Neighbor5_RSRP',
                           'Neighbor6_RSRP',
                           'Neighbor7_RSRP',
                           'Neighbor8_RSRP']].notnull().astype('int').sum(axis=1)

df['Neighbor_MOD3_COUNT'] = df[['Neighbor1_IS_MOD3',
                                'Neighbor2_IS_MOD3',
                                'Neighbor3_IS_MOD3',
                                'Neighbor4_IS_MOD3',
                                'Neighbor5_IS_MOD3',
                                'Neighbor6_IS_MOD3',
                                'Neighbor7_IS_MOD3',
                                'Neighbor8_IS_MOD3']].sum(axis=1)

def feature_normalization(df, col_name):
    max_value = df[col_name].max()
    min_value = df[col_name].min()
    width = max_value - min_value
    df[col_name] = df[col_name].map(lambda x: (x - min_value) / width)

feature_normalization(df, 'ServingCell_RSRP')
feature_normalization(df, 'ServingCell_RSRQ')
for i in range(1, 9):
    feature_normalization(df, 'Neighbor' + str(i) + '_RSRP')
    feature_normalization(df, 'Neighbor' + str(i) + '_RSRQ')

df['ServingCell_RSRP']
df['Neighbor1_RSRP']

# 观察 RSRP 与 RSRQ的关系
sns.pairplot(df, x_vars=['ServingCell_RSRP'], y_vars='ServingCell_RSRQ')

# 观察 'ServingCell_RSRP','ServingCell_RSRQ','ServingCell_PCI'与最终结果SINR的关系
sns.pairplot(df, x_vars=['ServingCell_RSRP', 'ServingCell_RSRQ', 'ServingCell_PCI'], y_vars='SINR')

# 观察邻区与预测结果的关系
sns.pairplot(
    df,
    x_vars=[
        'Neighbor2_RSRP',
        'Neighbor2_RSRQ',
        'Neighbor2_PCI',
        'Neighbor2_IS_MOD3'],
    y_vars='SINR')

sns.pairplot(
    df,
    x_vars=[
        'Neighbor3_RSRP',
        'Neighbor3_RSRQ',
        'Neighbor3_PCI',
        'Neighbor3_IS_MOD3'],
    y_vars='SINR')

# 观察邻区数量，MOD3数量，以及区域类型area与预测结果的关系
sns.pairplot(df, x_vars=['area', 'Neighbor_COUNT', 'Neighbor_MOD3_COUNT'], y_vars='SINR')

# 观察邻区MOD3与预测结果的关系
sns.pairplot(df, x_vars=['Neighbor1_IS_MOD3', 'Neighbor2_IS_MOD3', 'Neighbor3_IS_MOD3',
                         'Neighbor4_IS_MOD3', 'Neighbor5_IS_MOD3', 'Neighbor6_IS_MOD3',
                         'Neighbor7_IS_MOD3', 'Neighbor8_IS_MOD3'], y_vars='SINR')

# 选取与SINR有关系的特征
X = df[['area','ServingCell_RSRP', 'ServingCell_RSRQ', 'Neighbor1_RSRP', 'Neighbor1_RSRQ',
        'Neighbor1_IS_MOD3', 'Neighbor2_RSRP', 'Neighbor2_RSRQ' , 'Neighbor2_IS_MOD3',
        'Neighbor3_RSRP', 'Neighbor3_RSRQ', 'Neighbor3_IS_MOD3', 'Neighbor4_RSRP',
        'Neighbor4_RSRQ', 'Neighbor4_IS_MOD3', 'Neighbor5_RSRP', 'Neighbor5_RSRQ',
        'Neighbor5_IS_MOD3', 'Neighbor6_RSRP', 'Neighbor6_RSRQ', 'Neighbor6_IS_MOD3',
        'Neighbor7_RSRP', 'Neighbor7_RSRQ', 'Neighbor7_IS_MOD3', 'Neighbor8_RSRP',
        'Neighbor8_RSRQ', 'Neighbor8_IS_MOD3', 'Neighbor_COUNT', 'Neighbor_MOD3_COUNT']]

X.ServingCell_RSRQ = X.ServingCell_RSRQ.fillna(X.ServingCell_RSRQ.mean())
X = X.fillna(0)
y = df['SINR']

# area转为OneHot编码
X = pd.get_dummies(X,columns=['area'])

# 训练标准化
x_sds = StandardScaler()
x_sds.fit(X)

# 拆分训练集、测试集
X_train,X_test,y_train,y_test = train_test_split(X,y)
df0 = df.loc[X_test.index]

# 标准化处理训练集
X_train = x_sds.transform(X_train)

# 测试集标准化
X_test = x_sds.transform(X_test)

# 整表查缺失
X.isnull().any()

# 检查形状
X_train.shape,X_test.shape,y_train.shape,y_test.shape

# 多轮超参搜索，惩罚系数alpha = 970 相对较好
param_grid = {"alpha":np.arange(1,1300,50)}
gs = GridSearchCV(Ridge(),param_grid,cv=5)
gs.fit(X_train,y_train)

# 输出最佳参数
print(gs.best_params_)
print(gs.score(X_test,y_test))

# 使用最佳参数进行预测岭回归预测
m1 = Ridge(alpha=51)
m1.fit(X_train,y_train)

# 评估预测误差
y_pred = m1.predict(X_test)
mse = mean_squared_error(y_pred,y_test)
mse


