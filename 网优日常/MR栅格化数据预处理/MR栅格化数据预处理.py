# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 11:13:40 2020

@author: Administrator
"""
import pandas as pd
import os


path =r'D:\_python小程序\MR栅格化数据预处理'
os.chdir(path)

file_name = 'QJ小区栅格10月.csv'
# =============================================================================
# 通过生成器读取大型 excel 文件
# =============================================================================
def read_csv_partly(file):
    file_data = pd.read_csv(file, engine='python', encoding='utf-8', chunksize=50000)
    for df_tmp in file_data:
        yield df_tmp


def chose_color(rsrp):
    if rsrp >= -80:
        color = 'darkblue'
    if -80 > rsrp >= -95:
        color = 'blue'
    elif -95 > rsrp >= -105:
        color = 'green'
    elif -105 > rsrp >= -115:
        color = 'yellow'
    elif -115 > rsrp >= -125:
        color = 'red'
    elif -125 > rsrp:
        color = 'black'
    return color


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
df_res['cell_ind'] = df_res['eNB'].map(str) +'_'+df_res['CELLID'].map(str)
df_res['color'] =  df_res['AVG_SCRSRP'].map(lambda x:chose_color(x))

with open('QJ小区栅格10月_处理后.csv','w', newline = '') as f:
    df_res.to_csv(f,index =False)
#df_ql = pd.read_excel('ql_eci.xlsx')
#
#df_QL = df_res[df_res['SC_ECI'].isin(df_ql['ECI'])]
#with open('YX小区栅格9月.csv','w',newline = '') as f:
#    df_QL.to_csv(f,index =False)