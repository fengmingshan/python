# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 09:08:06 2018
制作查询SCTP脚本
@author: Administrator
"""
import pandas as pd

path = r'D:\诊断电压脚本'+'\\'
PM1 = 'PmDevice_OMMB1.xlsx'
PM2 = 'PmDevice_OMMB2.xlsx'
PM3 = 'PmDevice_OMMB3.xlsx'

PM_CMD1 = 'CMD_OMMB1.txt' 
PM_CMD2 = 'CMD_OMMB2.txt' 
PM_CMD3 = 'CMD_OMMB3.txt' 


df_PM1 = pd.read_excel(path + PM1,skiprows=1,encoding='utf-8') 
df_PM1 = df_PM1.drop([0,1])
df_PM1['对象描述'] = df_PM1['对象描述'].map(lambda x:x.split('.')[2][0:2])
df_PM1 = df_PM1.reset_index()
del df_PM1['index']

with open(path + PM_CMD1,'w',encoding='utf-8') as file:
    for i in range(0,len(df_PM1),1):
        line = 'BOARD DIAGNOSE:SUBNET={0},NE={1},RACK=1,SHELF=1,SLOT={2},FUNCTION_ID=16777224;'\
        .format(df_PM1.loc[i,'子网'],
                df_PM1.loc[i,'管理网元ID'],
                df_PM1.loc[i,'对象描述'])
        file.write(line+'\n')
        

df_PM2 = pd.read_excel(path + PM2,skiprows=1,encoding='utf-8') 
df_PM2 = df_PM2.drop([0,1])
df_PM2['对象描述'] = df_PM2['对象描述'].map(lambda x:x.split('.')[2][0:2])
df_PM2 = df_PM2.reset_index()
del df_PM2['index']

with open(path + PM_CMD2,'w',encoding='utf-8') as file:
    for i in range(0,len(df_PM2),1):
        line = 'BOARD DIAGNOSE:SUBNET={0},NE={1},RACK=1,SHELF=1,SLOT={2},FUNCTION_ID=16777224;'\
        .format(df_PM2.loc[i,'子网'],
                df_PM2.loc[i,'管理网元ID'],
                df_PM2.loc[i,'对象描述'])
        file.write(line+'\n')


df_PM3 = pd.read_excel(path + PM3,skiprows=1,encoding='utf-8') 
df_PM3 = df_PM3.drop([0,1])
df_PM3['对象描述'] = df_PM3['对象描述'].map(lambda x:x.split('.')[2][0:2])
df_PM3 = df_PM1.reset_index()
del df_PM3['index']

with open(path + PM_CMD3,'w',encoding='utf-8') as file:
    for i in range(0,len(df_PM3),1):
        line = 'BOARD DIAGNOSE:SUBNET={0},NE={1},RACK=1,SHELF=1,SLOT={2},FUNCTION_ID=16777224;'\
        .format(df_PM3.loc[i,'子网'],
                df_PM3.loc[i,'管理网元ID'],
                df_PM3.loc[i,'对象描述'])
        file.write(line+'\n')




