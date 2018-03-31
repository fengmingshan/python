# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 14:11:25 2018

@author: Administrator
"""
import pandas as pd 

data_path =  r'D:\2018年塔租稽核' + '\\'
old = '201712.xls'
new = '201801.xls'

df_old = pd.read_excel(data_path + old ,encoding = 'utf-8') 
df_new = pd.read_excel(data_path + new ,encoding = 'utf-8') 

col_old = list(df_old.columns)
col_new = list(df_new.columns)

both = list(set(col_old) & set(col_new))
both.remove('产品业务确认单编号')
df_result = pd.DataFrame(columns=['产品业务确认单编号'])
df_result['产品业务确认单编号'] = df_old['产品业务确认单编号']
df_merge = pd.merge(df_old,df_new,on='产品业务确认单编号',how='left')

for col in both:
    df_result[col + '_old'] = df_merge[col + '_x']
    df_result[col + '_new'] = df_merge[col + '_y']
    df_result[col + '_abnormal'] = ''
    for i in range(0,len(df_result),1):
        if  df_merge.loc[i,col + '_x'] == df_merge.loc[i,col + '_y']:
            df_result.loc[i,col + '_abnormal'] = '-'
        elif  df_merge.loc[i,col + '_x'] != df_merge.loc[i,col + '_y']:
            df_result.loc[i,col + '_abnormal'] = '异常'

writer = pd.ExcelWriter(data_path  + '核对结果.xls')
df_result.to_excel(writer,'核对结果') 
writer.save()
