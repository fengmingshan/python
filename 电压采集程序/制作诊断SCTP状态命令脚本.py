# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 09:08:06 2018
制作查询SCTP脚本
@author: Administrator
"""
import pandas as pd


path = r'D:\制作诊断脚本'+'\\'
sctp1='Sctp_20180422_095746281.xlsx'
sctp2='Sctp_20180422_095713812.xlsx'
file1='查询SCTP脚本_ommb1.txt' 
file2='查询SCTP脚本_ommb2.txt' 
df_sctp1 = pd.read_excel(path + sctp1,encoding='utf-8',skiprows = 1)
df_sctp1 = df_sctp1.drop([0,1])
df_sctp1 = df_sctp1[df_sctp1['SCTP链路号'] =='0']
df_sctp1.reset_index(inplace=True)
df_sctp1 = df_sctp1.drop('index',axis = 1 )

df_sctp2 = pd.read_excel(path + sctp2,encoding='utf-8',skiprows = 1) 
df_sctp2 = df_sctp2.drop([0,1])
df_sctp2 = df_sctp2[df_sctp2['SCTP链路号'] =='0']
df_sctp2.reset_index(inplace=True)
df_sctp2 = df_sctp2.drop('index',axis = 1 )

with open(path+file1,'a',encoding='utf-8') as f1:
    for i in range(0,len(df_sctp1),1):
        line = 'SHOW SCTP:SUBNET={0},NE={1},SCTP={2},RADIO={3};'.format(df_sctp1.loc[i,'子网'],df_sctp1.loc[i,'管理网元ID'],df_sctp1.loc[i,'SCTP对象ID'],df_sctp1.loc[i,'无线制式'])
        f1.write(line+'\n')

with open(path+file2,'a',encoding='utf-8') as f2 :
    for i in range(0,len(df_sctp2),1):
        line = 'SHOW SCTP:SUBNET={0},NE={1},SCTP={2},RADIO={3};'.format(df_sctp2.loc[i,'子网'],df_sctp2.loc[i,'管理网元ID'],df_sctp2.loc[i,'SCTP对象ID'],df_sctp2.loc[i,'无线制式'])
        f2.write(line+'\n')

