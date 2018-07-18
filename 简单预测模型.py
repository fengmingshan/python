# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:30:59 2018

@author: Administrator
"""
import pandas as pd

import numpy as np

from sklearn.preprocessing import LabelEncoder

import random  

from sklearn.ensemble import RandomForestClassifier 

from sklearn.ensemble import GradientBoostingClassifier

data_path = r'D:\试题宽带预测' + '\\'
train = pd.read_csv(data_path + 'broadband_train.csv', engine = 'python', encoding = 'gbk')
test = pd.read_csv(data_path +  'broadband_test.csv', engine = 'python', encoding = 'gbk')

test['BROADBAND'] = '' 
train['Type']= 'Train'
test['Type']= 'Test'

fullData =pd.concat([train,test],axis=0) #联合训练、测试数据集

fullData.columns # 显示所有的列名称
fullData.head(10) #显示数据框的前10条记录
fullData.describe() #你可以使用describe()函数查看数值域的概要

ID_col = ['CUST_ID']
target_col = ['BROADBAND']
cat_cols = ['GENDER','AUTOPAY']
num_cols = ['AGE','TENURE','CHANNEL','ARPU_3M','CALL_PARTY_CNT','DAY_MOU','AFTERNOON_MOU','NIGHT_MOU','AVG_CALL_LENGTH'] 

num_cat_cols = num_cols + cat_cols # 组合数值变量和分类变量

for var in num_cat_cols:   
    if fullData[var].isnull().any()==True:
        fullData[var+'_NA'] = fullData[var].isnull()*1

fullData[num_cols] = fullData[num_cols].fillna(fullData[num_cols].mean())
fullData.fillna(method='pad',inplace = True)

for var in cat_cols:
    number = LabelEncoder()    
    fullData[var] = number.fit_transform(fullData[var].astype('str'))
fullData["BROADBAND"] = number.fit_transform(fullData["BROADBAND"].astype('str'))
train=fullData[fullData['Type']=='Train']
test=fullData[fullData['Type']=='Test']
train['is_train'] = np.random.uniform(0, 1, len(train)) <= .75
Train, Validate = train[train['is_train']==True], train[train['is_train']==False]

other_col = ['Type','is_train'] 
features=list(set(list(fullData.columns))-set(ID_col)-set(target_col)-set(cat_cols)-set(other_col))
x_train = Train[list(features)].values
y_train = Train["BROADBAND"].values
x_validate = Validate[list(features)].values
y_validate = Validate["BROADBAND"].values

x_test=test[list(features)].values
random.seed(100)
rf = RandomForestClassifier(n_estimators=1000)
rf.fit(x_train, y_train)

status = rf.predict_proba(x_validate)
#fpr, tpr, _ = roc_curve(y_validate, status[:,1])

#roc_auc = auc(fpr, tpr)

#print(roc_auc)

final_status = rf.predict_proba(x_test)

test["BROADBAND"]=final_status[:,1]

test.to_csv(data_path + 'out.csv',columns=['CUST_ID','BROADBAND'])
