# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 09:34:13 2018

@author: Administrator
"""

import pandas as pd 
import os
from datetime import datetime 
current_date = str(datetime.now()).split('.')[0].split(' ')[0]

data_path = r'd:\2019年工作\2019年4月NB小区关断节能' + '\\'

file_ommb1 = 'ECellEquipmentFunctionNB_OMMB1.xlsx'
file_ommb2 = 'ECellEquipmentFunctionNB_OMMB2.xlsx'
file_ommb3 = 'ECellEquipmentFunctionNB_OMMB3.xlsx'


# =============================================================================
# 生成ommb1修改指令
# =============================================================================
df_ommb1 = pd.read_excel(data_path + file_ommb1 ,encoding='utf-8') 
df_ommb1['MOI'] = df_ommb1['MOI'].map(lambda x:x.replace('ConfigSet=0,',''))

with open(data_path + current_date + '_' + 'apply_right_OMMB1.txt','a') as f:
    for i in range(0,len(df_ommb1),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_ommb1.loc[i,'SubNetwork'],
                df_ommb1.loc[i,'MEID'],
)
        f.write(line+'\n')         


with open(data_path + current_date + '_'  + 'OMMB1_chang_NBCellPower.txt','a') as f:
    for i in range(0,len(df_ommb1),1):                                                           
        line = r'UPDATE:MOC="ECellEquipmentFunctionNB",MOI="{0}",ATTRIBUTES="cpTransPwr=10.0",EXTENDS="";'\
        .format(df_ommb1.loc[i,'MOI'])
        f.write(line+'\n') 

# =============================================================================
# 生成ommb2修改指令
# =============================================================================
df_ommb2 = pd.read_excel(data_path + file_ommb2 ,encoding='utf-8') 
df_ommb2['MOI'] = df_ommb2['MOI'].map(lambda x:x.replace('ConfigSet=0,',''))

with open(data_path + current_date + '_'  + 'apply_right_OMMB2.txt','a') as f:
    for i in range(0,len(df_ommb2),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_ommb2.loc[i,'SubNetwork'],
                df_ommb2.loc[i,'MEID'],
)
        f.write(line+'\n')         


with open(data_path + current_date + '_'  + 'OMMB2_chang_NBCellPower.txt','a') as f:
    for i in range(0,len(df_ommb2),1):
        line = r'UPDATE:MOC="ECellEquipmentFunctionNB",MOI="{0}",ATTRIBUTES="cpTransPwr=10.0",EXTENDS="";'\
        .format(df_ommb2.loc[i,'MOI'],)
        f.write(line+'\n') 

# =============================================================================
# 生成ommb3修改指令
# =============================================================================
df_ommb3 = pd.read_excel(data_path + file_ommb3 ,encoding='utf-8') 
df_ommb3['MOI'] = df_ommb3['MOI'].map(lambda x:x.replace('ConfigSet=0,',''))

with open(data_path + current_date + '_'  + 'apply_right_OMMB3.txt','a') as f:
    for i in range(0,len(df_ommb3),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_ommb3.loc[i,'SubNetwork'],
                df_ommb3.loc[i,'MEID'],
)
        f.write(line+'\n')         


with open(data_path + current_date + '_'  + 'OMMB3_chang_NBCellPower.txt','a') as f:
    for i in range(0,len(df_ommb3),1):
        line = r'UPDATE:MOC="ECellEquipmentFunctionNB",MOI="{0}",ATTRIBUTES="cpTransPwr=10.0",EXTENDS="";'\
        .format(df_ommb3.loc[i,'MOI'])
        f.write(line+'\n') 
