# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 20:59:40 2018
诊断PM板命令脚本
@author: Administrator
"""
import pandas as pd

# =============================================================================
# 设置环境变量
# =============================================================================
data_path = r'D:\4G_voltage' + '\\'
ommb1_file = 'PmDevice_ommb1.xls' 
ommb2_file = 'PmDevice_ommb2.xls' 

df_ommb1 = pd.read_excel(data_path + ommb1_file,dtype = 'str',encoding = 'utf-8' )

df_ommb2 = pd.read_excel(data_path + ommb2_file,dtype = 'str',encoding = 'utf-8' )

# 生成OMMB1的命令
with open(data_path + 'pm_command_ommb1.txt','a',encoding='utf-8') as F:
    for i in range(0,len(df_ommb1),1):
        command = 'BOARD DIAGNOSE:SUBNET=' + df_ommb1.loc[i,'子网'] +  ',NE=' + df_ommb1.loc[i,'管理网元ID'] +\
        ',RACK=' + df_ommb1.loc[i,'RACK'] + ',SHELF=' + df_ommb1.loc[i,'SHELF'] + ',SLOT=' +\
        df_ommb1.loc[i,'SLOT'] + ',FUNCTION_ID=16777224;'
        F.write(command+'\n')


# 生成OMMB2的命令
with open(data_path + 'pm_command_ommb2.txt','a',encoding='utf-8') as F:
    for i in range(0,len(df_ommb2),1):
        command = 'BOARD DIAGNOSE:SUBNET=' + df_ommb2.loc[i,'子网'] +  ',NE=' + df_ommb2.loc[i,'管理网元ID'] +\
        ',RACK=' + df_ommb2.loc[i,'RACK'] + ',SHELF=' + df_ommb2.loc[i,'SHELF'] + ',SLOT=' +\
        df_ommb2.loc[i,'SLOT'] + ',FUNCTION_ID=16777224;'
        F.write(command+'\n')


    

