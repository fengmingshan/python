# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:39:32 2019

@author: Administrator
"""

import pandas as pd 
import numpy as np
import os
from datetime import datetime 
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

def 填写退服小区(a,b):
	if pd.isnull(a):
		return b.split('_')[0] + '_' + b.split('_')[1]
	else:
		return a 


current_date = str(datetime.now()).split('.')[0].split(' ')[0]

data_path = r'D:\2019年工作\2019年4月小区退服指标计算（新）' + '\\'
pic_path = r'D:\2019年工作\2019年4月小区退服指标计算（新）\PIC' + '\\'

all_files = os.listdir(data_path)
files = [x for x in all_files if 'alarm_cel_exit_service_child' in x] 

df_ALL = pd.DataFrame()
for file in files :
    df_tmp = pd.read_excel(data_path + file,skiprows = 1)
    df_ALL= df_ALL.append(df_tmp)
df_ALL = df_ALL.reset_index()
df_ALL.drop('index',axis = 1,inplace = True)

df_LTE = df_ALL[(df_ALL['是否NB小区'] == '否') | (df_ALL['是否NB小区'].isnull() == True) ] 

df_LTE.columns
df_LTE['退服小区标识'] = df_LTE.apply(lambda x : 填写退服小区(x.关联小区标识,x.告警对象名称),axis = 1)
df_LTE['LTE小区个数'] = df_LTE['LTE小区个数'].map(lambda x : 1 if pd.isnull(x) else x)

# =============================================================================
# 计算各县累计断站时长
# =============================================================================

with  pd.ExcelWriter(data_path + 'LTE原始数据.xlsx')  as writer:  #输出到excel
    df_LTE.to_excel(writer,'LTE原始数据',index=False) 

    
