# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 17:44:42 2018

@author: 1
"""

import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model

data_path = r'D:\_python\python\SINR值预测' + '\\'
df = pd.read_csv(data_path + 'MR_city.csv',engine = 'python')
df = df.fillna(0)
df['Neighbor1_MOD3']=df['Neighbor1_MOD3'].astype('bool')
df['Neighbor2_MOD3']=df['Neighbor2_MOD3'].astype('bool')
df['Neighbor3_MOD3']=df['Neighbor3_MOD3'].astype('bool')
df['is MOD3']=df['Neighbor1_MOD3']|df['Neighbor2_MOD3']|df['Neighbor3_MOD3']

# 保存标签备用
feature_list = list(df.columns)

# 在特征中去掉标签
df= df.drop('序号', axis = 1)
df= df.drop('SINR', axis = 1)
for i in range(1,9,1):
    df.drop('Neighbor'+ str(i) + '_MOD3',axis=1,inplace = True )
df= df.drop('ServingCell_PCI', axis = 1)

for i in range(1,9,1):
    df= df.drop('Neighbor'+ str(i) + '_pci', axis = 1)

# 名字单独保存一下，以备后患
df_list = list(df.columns)

# 转换成合适的格式
df = np.array(df)

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df,labels, random_state=1)

print(X_train.shape)
print (y_train.shape)
print (X_test.shape)
print (y_test.shape)

from sklearn.linear_model import LinearRegression
linreg = LinearRegression()
print(linreg.fit(X_train, y_train))

print (linreg.intercept_)
print (linreg.coef_)

# =============================================================================
# 评估模型
# =============================================================================
# 预测结果
predictions = linreg.predict(X_test)

# 计算误差
errors = abs(predictions - y_test)

# 计算 MAPE:因为分母test_labels中有为零的值，所以需要在计算是预先删除，否则会出现无穷大的值
new_errors = [] 
new_y_test = [] 
for i in range(0,len(test_labels),1):
    if test_labels[i] != 0:
        new_errors.append(errors[i])
        new_y_test.append(y_test[i])
new_errors = np.array(new_errors)
new_y_test = np.array(new_y_test)
# mean absolute percentage error (MAPE)
mape = 100 * (new_errors / new_y_test)

from sklearn import metrics
print('预测SINR平均误差:', round(np.mean(errors), 2), 'dB.')
# 用scikit-learn计算MSE
print ("RMSE:",np.sqrt(metrics.mean_squared_error(y_test, predictions)))
# 计算 MAPE
print ('MAPE:',np.median(mape),'%')
# 预测准确率 
print ('预测准确率:',100 - np.median(mape),'%' )

#做ROC曲线,对比真实值和预测值之间的变化
plt.figure(figsize=(40, 15))
plt.plot(range(len(predictions[:100])),predictions[:100],'b',linewidth=5,label="predict")
plt.plot(range(len(y_test[:100])),y_test[:100],'r',linewidth=5,label="test")
plt.legend(loc="upper right") #显示图中的标签
plt.xlabel("POINT")
plt.ylabel('SINR_value')
plt.show()