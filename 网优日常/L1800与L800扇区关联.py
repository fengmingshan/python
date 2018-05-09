# -*- coding: utf-8 -*-
"""
Created on Wed May  9 14:48:21 2018

@author: Administrator
"""
import pandas as pd

data_path = r'd:\test' +'\\'
L1800 = 'L1800与L800匹配_筛选.xlsx'
L800 = 'L800.xlsx'

df_L1800 = pd.read_excel(data_path + L1800, encoding='utf-8') 
df_L1800 =  df_L1800[['CELLNAME','CELLID','计算距离(米)','方位角','匹配基站']]
df_L1800['角度差'] = ''
df_L1800['匹配_CELLID'] = ''
df_L1800['匹配_CELLNAME'] = ''

df_L800  = pd.read_excel(data_path + L800, encoding='utf-8') 

for i in range(0,len(df_L1800),1):
    df_L800_tmp = df_L800[df_L800['CELLID'].str.contains(str(df_L1800.loc[i,'匹配基站']))]
    df_L800_tmp = df_L800_tmp.reset_index()
    del df_L800_tmp['index']
    degree = 360
    cell_id = ''
    cell_name = ''
    if len(df_L800_tmp)> 0:
        for j in range(0,len(df_L800_tmp),1):
            degree_tmp = abs(df_L1800.loc[i,'方位角'] - df_L800_tmp.loc[j,'方位角'])
            if degree_tmp < degree:
                degree = degree_tmp
                cell_id = df_L800_tmp.loc[j,'CELLID']
                cell_name = df_L800_tmp.loc[j,'CELLNAME']
    df_L1800.loc[i,'角度差'] = degree
    df_L1800.loc[i,'匹配_CELLID'] = cell_id
    df_L1800.loc[i,'匹配_CELLNAME'] = cell_name

with pd.ExcelWriter(data_path + '匹配结果.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_L1800.to_excel(writer,'匹配结果') 

            
            
    