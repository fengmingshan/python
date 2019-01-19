# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 09:08:25 2019

@author: Administrator
"""

import pandas as pd 
import os


data_path = r'D:\CQI报表' + '\\'

PhyChannel1 = 'PhyChannel_OMMB1.xlsx' 
PhyChannel2 = 'PhyChannel_OMMB2.xlsx'

df_OMMB1 = pd.read_excel(data_path + PhyChannel1 ,encoding='utf-8') 
df_OMMB1 = df_OMMB1.drop([0,1,2])

df_OMMB2 = pd.read_excel(data_path + PhyChannel2 ,encoding='utf-8') 
df_OMMB2 = df_OMMB2.drop([0,1,2])


# =============================================================================
# 生成ommb1修改指令
# =============================================================================
df_OMMB1 =  df_OMMB1[df_OMMB1['cqiRptPeriod']!='1;3;5']
df_OMMB1 = df_OMMB1.reset_index()

with open(out_path + 'apply_right_OMMB1.txt','w') as f:
    for i in range(0,len(df_OMMB1),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_OMMB1.loc[i,'SubNetwork'],
                df_OMMB1.loc[i,'MEID'],
)
        f.write(line+'\n')         

with open(out_path + 'OMMB1_command.txt','w') as f:
    for i in range(0,len(df_OMMB1),1):
        line = r'UPDATE:MOC="PhyChannel",MOI="{0}",ATTRIBUTES="cqiRptPeriod=\"1;3;5\"",EXTENDS="";'\
        .format(df_OMMB1.loc[i,'MOI'])
        f.write(line+'\n') 
        
# =============================================================================
# 生成ommb2修改指令
# =============================================================================
df_OMMB2 =  df_OMMB2[df_OMMB2['cqiRptPeriod']!='1;3;5']
df_OMMB2 = df_OMMB2.reset_index()
with open(out_path + 'apply_right_OMMB2.txt','w') as f:
    for i in range(0,len(df_OMMB2),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_OMMB2.loc[i,'SubNetwork'],
                df_OMMB2.loc[i,'MEID'],
)
        f.write(line+'\n')         


with open(out_path + 'OMMB2_command.txt','w') as f:
    for i in range(0,len(df_OMMB2),1):
        line = r'UPDATE:MOC="PhyChannel",MOI="{0}",ATTRIBUTES="cqiRptPeriod=\"1;3;5\"",EXTENDS="";'\
        .format(df_OMMB2.loc[i,'MOI'])
        f.write(line+'\n') 

