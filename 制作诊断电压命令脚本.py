# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 09:08:06 2018
制作查询SCTP脚本
@author: Administrator
"""
import pandas as pd

path = r'D:\诊断电压脚本'+'\\'
PM = 'PmDevice_20180415_160732343.xlsx'
CMD = 'CMD.txt' 

df_PM = pd.read_excel(path + PM,skiprows=1,encoding='utf-8') 
df_PM = df_PM.drop([0,1])
df_PM['对象描述'] = df_PM['对象描述'].map(lambda x:x.split('.')[2][0:2])
df_PM = df_PM.reset_index()
del df_PM['index']

with open(path + CMD,'w',encoding='utf-8') as file:
    for i in range(0,len(df_PM),1):
        line = 'BOARD DIAGNOSE:SUBNET={0},NE={1},RACK=1,SHELF=1,SLOT={2},FUNCTION_ID=16777224;'.format(df_PM.loc[i,'子网'],df_PM.loc[i,'管理网元ID'],df_PM.loc[i,'对象描述'])
        file.write(line+'\n')


