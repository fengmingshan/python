# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 09:34:13 2018

@author: Administrator
"""

import pandas as pd 
import os
from datetime import datetime 
current_date = str(datetime.now()).split('.')[0].split(' ')[0]

data_path = r'D:\test' + '\\'

file_name = '修改NB小区功率_2019-04-19.xlsx'
df_file = pd.read_excel(data_path + file_name ,encoding='utf-8') 

# =============================================================================
# 生成ommb1修改指令
# =============================================================================
df_ommb1 = df_file[df_file['OMMB'] == 'OMMB1']
df_ommb1 = df_ommb1.reset_index()


with open(data_path + current_date + '_' + 'apply_right_OMMB1.txt','a') as f:
    for i in range(0,len(df_ommb1),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_ommb1.loc[i,'SubNetwork'],
                df_ommb1.loc[i,'MEID'],
)
        f.write(line+'\n')         


with open(data_path + current_date + '_'  + 'OMMB1_command.txt','a') as f:
    for i in range(0,len(df_ommb1),1):
        line = r'UPDATE:MOC="EUtranCellFDD",MOI="{0}",ATTRIBUTES="flagSwiMode=6",EXTENDS="";'\
        .format(df_ommb1.loc[i,'MOI'])
        f.write(line+'\n') 

# =============================================================================
# 生成ommb1修改指令
# =============================================================================
df_ommb2 = df_file[df_file['OMMB'] == 'OMMB2']
df_ommb2 = df_ommb2.reset_index()


with open(data_path + current_date + '_'  + 'apply_right_OMMB2.txt','a') as f:
    for i in range(0,len(df_ommb2),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_ommb2.loc[i,'SubNetwork'],
                df_ommb2.loc[i,'MEID'],
)
        f.write(line+'\n')         


with open(data_path + current_date + '_'  + 'OMMB2_command.txt','a') as f:
    for i in range(0,len(df_ommb2),1):
        line = r'UPDATE:MOC="EUtranCellFDD",MOI="{0}",ATTRIBUTES="flagSwiMode=6",EXTENDS="";'\
        .format(df_ommb2.loc[i,'MOI'])
        f.write(line+'\n') 
