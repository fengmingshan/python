# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 08:41:33 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import random  

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve
from sklearn import tree
data_path = r'D:\试题宽带预测' + '\\'
train = pd.read_csv(data_path + 'broadband_train.csv', engine = 'python', encoding = 'gbk')
test = pd.read_csv(data_path +  'broadband_test.csv', engine = 'python', encoding = 'gbk')

train['GENDER'] = train['GENDER'].map(lambda x:x.replace('男','1'))
train['GENDER'] = train['GENDER'].map(lambda x:x.replace('女','0'))
test['GENDER'] = test['GENDER'].map(lambda x:x.replace('男','1'))
test['GENDER'] = test['GENDER'].map(lambda x:x.replace('女','0'))
train['AUTOPAY'] = train['AUTOPAY'].map(lambda x:x.replace('是','1'))
train['AUTOPAY'] = train['AUTOPAY'].map(lambda x:x.replace('否','0'))
test['AUTOPAY'] = test['AUTOPAY'].map(lambda x:x.replace('是','1'))
test['AUTOPAY'] = test['AUTOPAY'].map(lambda x:x.replace('否','0'))

ID_col = ['CUST_ID']
target_col = ['BROADBAND']
cat_cols = ['GENDER','AUTOPAY']
num_cols = ['AGE','TENURE','CHANNEL','ARPU_3M','CALL_PARTY_CNT','DAY_MOU','AFTERNOON_MOU','NIGHT_MOU','AVG_CALL_LENGTH'] 

num_cat_cols = num_cols + cat_cols # 组合数值变量和分类变量

train.fillna(method='pad',inplace = True)
test.fillna(method='pad',inplace = True)

train_data = train[num_cat_cols]
train_target =  train['BROADBAND']
test_data = test[num_cat_cols]

x_train,x_test, y_train, y_test = train_test_split(train_data,train_target,test_size=0.4, random_state=0) 
clf=tree.DecisionTreeClassifier(criterion='entropy')
clf.fit(x_train,y_train)

precision,recall,thresholds=precision_recall_curve(y_train,clf.predict(x_train))
print (precision,recall,thresholds)

final_status = clf.predict_proba(test_data)[:,1]
out = pd.DataFrame()
out['CUST_ID'] = test['CUST_ID']
out['BROADBAND'] = ''
out['BROADBAND'] =  final_status
out.to_csv(data_path + 'out.csv',columns=['CUST_ID','BROADBAND'])
