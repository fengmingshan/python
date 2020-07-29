# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 11:13:40 2020

@author: Administrator
"""
import pandas as pd
import os


path =r'D:\_python小程序\MR栅格化数据分析'
os.chdir(path)

# =============================================================================
# 通过生成器读取大型 excel 文件
# =============================================================================
def read_csv_partly(file):
    file_data = pd.read_csv(file, engine='python', encoding='utf-8', chunksize=50000)
    for df_tmp in file_data:
        yield df_tmp


list_df =[]
i = 1
for df in read_csv_partly('qujing_grid50_cell_day.csv'):
    list_df.append(df)
    print('已读取: {}W条。'.format(i*5))
    i += 1
df_res = pd.concat(list_df,axis = 0)
df_res.columns
cols = ['SDATE', 'CITY', 'SC_ECI', 'GRIDX', 'GRIDY', 'NUM_HOURS', 'AVG_SCRSRP',
       'RSRP_SAMPLES', 'AVG_SCRSRQ', 'RSRQ_SAMPLES', 'AVG_ULSINR',
       'ULSINR_SAMPLES', 'AVG_TA', 'TA_SAMPLES', 'FREQ', 'EARFCN']

df_ql = pd.read_excel('ql_eci.xlsx')

df_QL = df_res[df_res['SC_ECI'].isin(df_ql['ECI'])]
with open('栅格化数据_麒麟区.csv','w',newline = '') as f:
    df_QL.to_csv(f,index =False)