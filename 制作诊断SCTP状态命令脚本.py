# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 09:08:06 2018
制作查询SCTP脚本
@author: Administrator
"""
import pandas as pd


path = r'D:\2018年工作\2018年LTE断站管控'+'\\'
sctp1='SCTP_1.xls'
sctp2='SCTP_2.xls'
file1='查询SCTP脚本_ommb1.txt' 
file2='查询SCTP脚本_ommb2.txt' 
df_sctp1 = pd.read_excel(path + sctp1,encoding='utf-8') 
df_sctp2 = pd.read_excel(path + sctp2,encoding='utf-8') 


f1=open(path+file1,'a',encoding='utf-8')
for i in range(0,len(df_sctp1),1):
    line = 'SHOW SCTP:SUBNET={0},NE={1},SCTP={2},RADIO={3};'.format(df_sctp1.loc[i,'子网'],df_sctp1.loc[i,'管理网元ID'],df_sctp1.loc[i,'SCTP对象ID'],df_sctp1.loc[i,'无线制式'])
    f1.write(line+'\n')
f1.close()

f2=open(path+file2,'a',encoding='utf-8')
for i in range(0,len(df_sctp2),1):
    line = 'SHOW SCTP:SUBNET={0},NE={1},SCTP={2},RADIO={3};'.format(df_sctp2.loc[i,'子网'],df_sctp2.loc[i,'管理网元ID'],df_sctp2.loc[i,'SCTP对象ID'],df_sctp2.loc[i,'无线制式'])
    f2.write(line+'\n')
f2.close()


