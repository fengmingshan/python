# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 23:43:53 2019

@author: Administrator
"""

'''
宽带用户离网预测，完成模型训练之后
使用shap库对模型进行解释，试图分析各个特征对预测结果的影响的程度
'''

from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
data_path = 'D:/_python/神经网络数据集/宽带离网预测'
os.chdir(data_path)

df1 = pd.read_csv('broadband_train.csv', engine='python')
df2 = pd.read_csv('broadband_test.csv', engine='python')
Y = df1['BROADBAND']
df1 = df1.iloc[:,:12]

df = df1.append(df2)
df.reset_index(inplace = True)
# =============================================================================
# 数据清洗
# =============================================================================
df.isnull().any()
df.dtypes
df = pd.get_dummies(df, columns=['GENDER'])
df = pd.get_dummies(df, columns=['AUTOPAY'])
df['GENDER_男'] = df['GENDER_男'].astype(int)
df['GENDER_女'] = df['GENDER_男'].astype(int)
df['AUTOPAY_是'] = df['GENDER_男'].astype(int)
df['AUTOPAY_否'] = df['GENDER_男'].astype(int)

df.columns

df['ARPU_3M'] = df['ARPU_3M'].fillna(df['ARPU_3M'].mean())
df['DAY_MOU'] = df['DAY_MOU'].fillna(df['DAY_MOU'].mean())
df['AFTERNOON_MOU'] = df['AFTERNOON_MOU'].fillna(df['AFTERNOON_MOU'].mean())
df['NIGHT_MOU'] = df['NIGHT_MOU'].fillna(df['NIGHT_MOU'].mean())
df['ARPU_3M'] = df['ARPU_3M'].fillna(df['ARPU_3M'].mean())

df['AGE'] = df['AGE'].fillna(df['AGE'].median())
df['CALL_PARTY_CNT'] = df['CALL_PARTY_CNT'].fillna(df['AGE'].median())
df['TENURE'] = df['TENURE'].fillna(df['AGE'].median())
df.isnull().any()
df.dtypes

df = df[['CUST_ID', 'AGE', 'TENURE', 'CHANNEL', 'ARPU_3M', 'CALL_PARTY_CNT',
       'DAY_MOU', 'AFTERNOON_MOU', 'NIGHT_MOU', 'AVG_CALL_LENGTH',
       'GENDER_女', 'GENDER_男', 'AUTOPAY_否', 'AUTOPAY_是']]

X = df.iloc[:len(df1), :13]
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.15, random_state=0)

# =============================================================================
#  导入算法
# =============================================================================
rf = RandomForestRegressor(n_estimators=1000, random_state=42)
rf.fit(X_train, y_train)

# =============================================================================
# 评估模型
# =============================================================================
# 测试模型
predictions = rf.predict(X_test)

# 计算误差
errors = abs(predictions - y_test)
print(np.mean(errors))

# =============================================================================
# 模型解释
# =============================================================================
import shap  # package used to calculate Shap values

row = 5
data_for_prediction = y_test.iloc[1]  # use 1 row of data here. Could use multiple rows if desired
data_for_prediction_array = data_for_prediction.reshape(1, -1)

# Create object that can calculate shap values
explainer = shap.TreeExplainer(rf)

# Calculate Shap values
shap_values = explainer.shap_values(data_for_prediction_array)

# 可视化
shap.initjs()
shap.force_plot(explainer.expected_value, shap_values[0,:], data_for_prediction_array)
