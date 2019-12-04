# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 19:05:35 2019

@author: Administrator
"""

@@ -0,0 +1,116 @@
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:47:08 2018

@author: Administrator
"""

import pandas as pd
import matplotlib.pyplot as plt

data_path = r'D:\_python\python\SINR值预测' + '\\'


df = pd.read_csv(data_path + 'MR_city.csv',engine = 'python')
df.fillna({'Neighbor1_RSRP':-128,'Neighbor2_RSRP':-128,'Neighbor3_RSRP':-128,'Neighbor4_RSRP':-128,'Neighbor5_RSRP':-128,'Neighbor6_RSRP':-128,'Neighbor7_RSRP':-128,'Neighbor8_RSRP':-128},inplace = True )
df.fillna({'Neighbor1_RSRQ':-30,'Neighbor2_RSRQ':-30,'Neighbor3_RSRQ':-30,'Neighbor4_RSRQ':-30,'Neighbor5_RSRQ':-30,'Neighbor6_RSRQ':-30,'Neighbor7_RSRQ':-30,'Neighbor8_RSRQ':-30},inplace = True )
df.fillna('0',inplace =True)

# 将所有MOD3项进行bool值处理
for i in range(1,3,1):
   df['Neighbor' + str(i) + '_MOD3']=df['Neighbor' + str(i) + '_MOD3'].astype('bool')

# 合并所有MOD3项
df['is_MOD3']=df['Neighbor1_MOD3']|df['Neighbor2_MOD3']|df['Neighbor3_MOD3']

# 因为MOD3干扰项已经被我们合并，所以可以删除
for i in range(1,9,1):
   df.drop('Neighbor'+ str(i) + '_MOD3',axis=1,inplace = True )

# 数据与标签
import numpy as np

# 标签
labels = np.array(df['SINR'])

# 在特征中去掉标签
df= df.drop('SINR', axis = 1)
df= df.drop('序号', axis = 1)
df= df.drop('ServingCell_PCI', axis = 1)
for i in range(1,9,1):
    df= df.drop('Neighbor'+ str(i) + '_pci', axis = 1)

df.info()
df.to_csv(data_path + '清洗结果.csv')


# 特征名字留着备用
feature_list = list(df.columns)


# 转换成合适的格式
df = np.array(df)

# 对源数据表格进行洗牌
#from sklearn.utils import shuffle
#df = shuffle(df)

# 数据集切分
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(df, labels, test_size = 0.25,random_state = 42)
print('训练集特征:', X_train.shape)
print('训练集标签:', y_train.shape)
print('测试集特征:', X_test.shape)
print('测试集标签:', y_test.shape)

# 导入算法
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators= 1000, random_state=42)
rf.fit(X_train, y_train)
# =============================================================================
# 评估模型
# =============================================================================
# 预测结果
predictions = rf.predict(X_test)

# 计算误差
errors = abs(predictions - y_test)

# 计算 MAPE:因为分母test_labels中有为零的值，所以需要在计算是预先删除，否则会出现无穷大的值
new_errors = [] 
new_y_test = [] 
for i in range(0,len(y_test),1):
    if y_test[i] != 0:
        new_errors.append(errors[i])
        new_y_test.append(y_test[i])
new_y_test = [abs(x) for x in new_y_test]        
new_errors = np.array(new_errors)
new_y_test = np.array(new_y_test)
# mean absolute percentage error (MAPE)
mape = 100 * (new_errors / new_y_test)
good_error = [x for x in errors if x < 6 ]
bad_error = [x for x in errors if x > 6 ]

from sklearn import metrics
print('预测SINR平均误差:', round(np.mean(errors), 2), 'dB.')
# 用scikit-learn计算MSE
print ("RMSE:",np.sqrt(metrics.mean_squared_error(y_test, predictions)))
# 计算 MAPE
print ('MAPE:',np.mean(mape),'%')
# 预测准确率 
print ('预测准确率:',100 - np.mean(mape),'%' )
# 预测靠谱率 
print ('预测靠谱率:',len(good_error)/len(errors)*100,'%' )
# 预测准确率 
print ('预测偏差率:',len(bad_error)/len(errors)*100,'%' )

#做ROC曲线,对比真实值和预测值之间的变化
plt.figure(figsize=(20, 4))
plt.plot(range(len(predictions[:100])),predictions[:100],'b',label="predict")
plt.plot(range(len(y_test[:100])),y_test[:100],'r',label="test")
plt.legend(loc="upper right") #显示图中的标签
plt.xlabel("POINT")
plt.ylabel('SINR_value')
plt.show()