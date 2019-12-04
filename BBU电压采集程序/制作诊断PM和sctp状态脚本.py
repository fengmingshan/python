# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 11:10:40 2018

@author: Administrator
"""
import pandas as pd

cmd_path = r'C:\Users\Administrator' + '\\'

# =============================================================================
# 制作诊断PM单板的命令脚本  
# =============================================================================
ommb1_file = 'PmDevice_20180422_095603250.xlsx' 
ommb2_file = 'PmDevice_20180422_095635750.xlsx' 
pm_cmd_ommb1 = 'CMD_OMMB1.txt'
pm_cmd_ommb2 = 'CMD_OMMB2.txt'

df_ommb1 = pd.read_excel(cmd_path + ommb1_file,dtype = 'str',encoding = 'utf-8',skiprows=1)
df_ommb2 = pd.read_excel(cmd_path + ommb2_file,dtype = 'str',encoding = 'utf-8',skiprows=1)

df_ommb1 = df_ommb1.drop([0,1])
df_ommb1['对象描述'] = df_ommb1['对象描述'].map(lambda x:x.split('.')[2][0:2])
df_ommb1 = df_ommb1.reset_index()
del df_ommb1['index']

df_ommb2 = df_ommb2.drop([0,1])
df_ommb2['对象描述'] = df_ommb2['对象描述'].map(lambda x:x.split('.')[2][0:2])
df_ommb2 = df_ommb2.reset_index()
del df_ommb2['index']
   
# 生成诊断OMMB1的命令
with open(cmd_path + pm_cmd_ommb1,'w',encoding='utf-8') as file:
    for i in range(0,len(df_ommb1),1):
        line = 'BOARD DIAGNOSE:SUBNET={0},NE={1},RACK=1,SHELF=1,SLOT={2},FUNCTION_ID=16777224;'.format(df_ommb1.loc[i,'子网'],df_ommb1.loc[i,'管理网元ID'],df_ommb1.loc[i,'对象描述'])
        file.write(line+'\n')


# 生成诊断OMMB2的命令
with open(cmd_path + pm_cmd_ommb2,'w',encoding='utf-8') as file:
    for i in range(0,len(df_ommb2),1):
        line = 'BOARD DIAGNOSE:SUBNET={0},NE={1},RACK=1,SHELF=1,SLOT={2},FUNCTION_ID=16777224;'.format(df_ommb2.loc[i,'子网'],df_ommb2.loc[i,'管理网元ID'],df_ommb2.loc[i,'对象描述'])
        file.write(line+'\n')

# =============================================================================
#  制作诊断SCTP状态的命令脚本   
# =============================================================================
sctp1='Sctp_20180422_095746281.xlsx'
sctp2='Sctp_20180422_095713812.xlsx'
file1='查询SCTP脚本_ommb1.txt' 
file2='查询SCTP脚本_ommb2.txt' 
df_sctp1 = pd.read_excel(cmd_path + sctp1,encoding='utf-8',skiprows = 1)
df_sctp1['无线制式'] = df_sctp1['无线制式'].map(lambda x:x.replace(';64',''))
df_sctp1 = df_sctp1.drop([0,1])
df_sctp1 = df_sctp1[df_sctp1['SCTP链路号'] =='0']
df_sctp1.reset_index(inplace=True)
df_sctp1 = df_sctp1.drop('index',axis = 1 )

df_sctp2 = pd.read_excel(cmd_path + sctp2,encoding='utf-8',skiprows = 1) 
df_sctp2['无线制式'] = df_sctp2['无线制式'].map(lambda x:x.replace(';64',''))
df_sctp2 = df_sctp2.drop([0,1])
df_sctp2 = df_sctp2[df_sctp2['SCTP链路号'] =='0']
df_sctp2.reset_index(inplace=True)
df_sctp2 = df_sctp2.drop('index',axis = 1 )

with open(cmd_path + file1,'w',encoding='utf-8') as f1:
    for i in range(0,len(df_sctp1),1):
        line = 'SHOW SCTP:SUBNET={0},NE={1},SCTP={2},RADIO={3};'.format(df_sctp1.loc[i,'子网'],df_sctp1.loc[i,'管理网元ID'],df_sctp1.loc[i,'SCTP对象ID'],df_sctp1.loc[i,'无线制式'])
        f1.write(line+'\n')
        
with open(cmd_path + file2,'w',encoding='utf-8') as f2 :
    for i in range(0,len(df_sctp2),1):
        line = 'SHOW SCTP:SUBNET={0},NE={1},SCTP={2},RADIO={3};'.format(df_sctp2.loc[i,'子网'],df_sctp2.loc[i,'管理网元ID'],df_sctp2.loc[i,'SCTP对象ID'],df_sctp2.loc[i,'无线制式'])
        f2.write(line+'\n')
