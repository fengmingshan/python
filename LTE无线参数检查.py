# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:57:26 2018
LTE参数检查
@author: Administrator
"""
import pandas  as pd 
import os

data_path = r'd:\2018年工作\2018年4月CQI专项\无线参数' + '\\'
out_path = r'd:\2018年工作\2018年4月CQI专项' + '\\'

df_cell = pd.read_excel(out_path + 'cell_id.xlsx',encoding = 'utf-8')

all_files = os.listdir(data_path)
for file in all_files:
    df_tmp = pd.read_excel(data_path + file,encoding = 'utf-8',skiprows = 1)
    df_tmp = df_tmp.drop([0,1])
    df_tmp['cell_id'] = df_tmp['管理网元ID'] + '_'  +  df_tmp['对象描述'].map(lambda x:x.split('=')[1])
    df_tmp = df_tmp.drop(['DN','管理网元ID','对象描述','最新修改时间'],axis=1)
    df_cell = pd.merge(df_cell,df_tmp,how = 'left', on = 'cell_id')
df_cell =  df_cell.drop(['结果','修改标记'],axis = 1) 

cell_A = '585328_132'
cell_B = '585329_129'
df_result = df_cell[(df_radio['cell_id']== cell_A)|(df_radio['cell_id']== cell_B)]
df_T = df_result.T
df_T['比较结果'] = ''
df_T.fillna('-',inplace = True)
df_T = df_T.reset_index()

for i in range(0,len(df_T),1):
    if df_T.loc[i,3] == df_T.loc[i,4]:
        df_T.loc[i,'比较结果'] = '-'
    else:
        df_T.loc[i,'比较结果'] = '不同'

with pd.ExcelWriter(out_path + '比较结果.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_T.to_excel(writer,'比较结果') 



