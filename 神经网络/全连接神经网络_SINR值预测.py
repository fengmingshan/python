# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:31:35 2019

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

# 整表查缺失
X.isnull().any()

# 拆分训练集、测试集
X_train,X_test,y_train,y_test = train_test_split(X,y)
df0 = df.loc[X_test.index]


# 检查形状
X_train.shape,X_test.shape,y_train.shape,y_test.shape

#神经网络
m4 = keras.Sequential()
m4.add(Dense(64,input_shape=(31,),activation='relu'))
m4.add(Dense(32,activation='relu'))
m4.add(Dense(16,activation='relu'))
m4.add(Dense(1))

m4.summary()

m4.compile(optimizer='adam', loss='mse', metrics=['mse'])
m4.fit(X_train,y_train,epochs=130,batch_size=64,validation_data=(X_test,y_test))

m4.save_weights('MLP_SINR_weights.h5')

# =============================================================================
# 加载模型
# =============================================================================
data_path = 'D:/Notebook/通过MR数据预测采样点SINR值'
os.chdir(data_path)
if not os.path.exists('./预测结果可视化'):
    os.mkdir('./预测结果可视化')
# 加载模型
model = keras.Sequential()
model.add(Dense(64,input_shape=(31,),activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(16,activation='relu'))
model.add(Dense(1))

model.summary()

model.load_weights('MLP_SINR_weights.h5')

# 预测
y_pred = model.predict(X_test)
print(y_pred[:10])

# =============================================================================
# 评估模型
# =============================================================================
mse = mean_squared_error(y_pred,y_test)
mse

# 测试集+预测结果进行业务校验
df0['y_real'] = df0['SINR']
df0['y_pred'] = y_pred
df0.eval('误差=y_pred-y_real',inplace=True)
df0.loc[abs(df0.误差)<=6,'误差分类'] = '6以内'
df0.loc[abs(df0.误差)>6,'误差分类'] = '6以上'
df0.head()

df0.误差分类.value_counts()

less_than_6dB = 1 - len(df0[df0['误差']>6])/len(df0[df0['误差']<=6])
less_than_3dB = 1 - len(df0[df0['误差']>3])/len(df0[df0['误差']<=3])
print('误差小于6dB的比例： {}'.format(less_than_6dB))
print('误差小于3dB的比例： {}'.format(less_than_3dB))

# 检查误差分布
sns.distplot(df0.误差);
np.mean(df0.误差),np.std(df0.误差)

# 查看预测值与真实值分布
sns.scatterplot(df0.y_real,df0.y_pred)
plt.savefig('./预测结果可视化/MLP_预测值与真实值分布.png', format='png', dpi=200)
plt.show()
plt.close()

# 绘制预测曲线
import matplotlib.pyplot as plt
%matplotlib inline

df0.reset_index(inplace =True)
df_draw = df0.loc[:100,:]

plt.figure(figsize=(50, 10))
df_draw[['y_real','y_pred']].plot(legend=True)
plt.savefig('./预测结果可视化/MLP_真实值和预测值曲线.png',format='png',dpi =200)
plt.show()
plt.close()

df0.to_csv('./预测结果可视化/MLP_验证集输出_神经网络.csv',index=False)