# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 11:13:40 2020

@author: Administrator
"""
import pandas as pd
import os


path =r'D:\_python小程序\MR栅格化数据分析'
os.chdir(path)

file_name = 'qujing_grid50_cell_day.csv'
# =============================================================================
# 通过生成器读取大型 excel 文件
# =============================================================================
def read_csv_partly(file):
    file_data = pd.read_csv(file, engine='python', encoding='utf-8', chunksize=50000)
    for df_tmp in file_data:
        yield df_tmp


list_df =[]
i = 1
for df in read_csv_partly(file_name):
    list_df.append(df)
    print('已读取: {}W条。'.format(i*5))
    i += 1
df_res = pd.concat(list_df,axis = 0)
df_res.columns
cols = ['SDATE', 'CITY', 'SC_ECI', 'GRIDX', 'GRIDY', 'NUM_HOURS', 'AVG_SCRSRP',
       'RSRP_SAMPLES', 'AVG_SCRSRQ', 'RSRQ_SAMPLES', 'AVG_ULSINR',
       'ULSINR_SAMPLES', 'AVG_TA', 'TA_SAMPLES', 'FREQ', 'EARFCN']

df_res['CELLID'] = df_res['SC_ECI'].map(lambda x:x%256)
df_res['eNB'] = df_res['SC_ECI'].map(lambda x:x//256)
df_res['cell_ind'] = df_res['eNB'].map(str) + '_' + df_res['CELLID'].map(str)

with open('预处理后栅格数据.csv','w', newline = '') as f:
    df_res.to_csv(f,index =False)