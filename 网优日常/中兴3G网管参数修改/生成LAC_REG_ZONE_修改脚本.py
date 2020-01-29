# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 14:55:04 2018

@author: Administrator
"""

import pandas as pd
import os

data_path = r'd:\_LAC修改脚本' + '\\'
CELL_info = '曲靖LAC划小_无线网_修改清单.xlsx'
df_CELL_info = pd.read_excel(data_path + CELL_info,encoding='utf-8')

df_BSC1 =  df_CELL_info[(df_CELL_info['bssid']=='BSC1')&(df_CELL_info['system']!='-')]
df_BSC1 =  df_BSC1.reset_index()  
df_BSC1.drop('index',axis = 1)
df_BSC1_LAC = df_BSC1[df_BSC1['修改后_LAC']!='不修改']
df_BSC1_LAC = df_BSC1_LAC.reset_index()
  
df_BSC2 =  df_CELL_info[(df_CELL_info['bssid']=='BSC2')&(df_CELL_info['system']!='-')]
df_BSC2 =  df_BSC2.reset_index() 
df_BSC2.drop('index',axis = 1)
df_BSC2_LAC = df_BSC2[df_BSC2['修改后_LAC']!='不修改']
df_BSC2_LAC = df_BSC2_LAC.reset_index()  

# =============================================================================
# BSC1修改脚本
# =============================================================================
with open(data_path  +  'Apply_right_BSC1.txt','w') as f:
    line_list = []
    for i in range(0,len(df_BSC1),1):
        line = 'APPLY CMRIGHT:SYSTEM={0};'\
        .format(df_BSC1.loc[i,'system'])
        line_list.append(line)
    line_list = list(set(line_list))   
    for line in  line_list:
        f.write(line+'\n')         
   
with open(data_path + 'FIX_LAC_BSC1.txt','w') as f:
    for i in range(0,len(df_BSC1_LAC),1):
        line = 'SET 1X_CELL:POS="{0}"-"{1}",LAC={2};'\
        .format(df_BSC1_LAC.loc[i,'system'],
                df_BSC1_LAC.loc[i,'cellid'],
                df_BSC1_LAC.loc[i,'修改后_LAC']                
)
        f.write(line+'\n') 

with open(data_path + 'FIX_REG-ZONE_BSC1.txt','w') as f:
    for i in range(0,len(df_BSC1),1):
        line = 'SET 1X_CELLSYSPARA:POS="{0}"-"{1}",REG_ZONE={2};'\
        .format(df_BSC1.loc[i,'system'],
                df_BSC1.loc[i,'cellid'],
                df_BSC1.loc[i,'修改后_REG_ZONE']                
)
        f.write(line+'\n') 

with open(data_path  +  'Release_right_BSC1.txt','w') as f:
    line_list = []
    for i in range(0,len(df_BSC1),1):
        line = 'RELEASE CMRIGHT:SYSTEM={0};'\
        .format(df_BSC1.loc[i,'system'])
        line_list.append(line)
    line_list = list(set(line_list))   
    for line in  line_list:
        f.write(line+'\n')         

# =============================================================================
# BSC2修改脚本
# =============================================================================
with open(data_path  +  'Apply_right_BSC2.txt','w') as f:
    line_list = []
    for i in range(0,len(df_BSC2),1):
        line = 'APPLY CMRIGHT:SYSTEM = {0};'\
        .format(df_BSC2.loc[i,'system'])
        line_list.append(line)
    line_list = list(set(line_list))   
    for line in  line_list:
        f.write(line+'\n')         
   
with open(data_path + 'FIX_LAC_BSC2.txt','w') as f:
    for i in range(0,len(df_BSC2_LAC),1):
        line = 'SET 1X_CELL:POS="{0}"-"{1}",LAC={2};'\
        .format(df_BSC2_LAC.loc[i,'system'],
                df_BSC2_LAC.loc[i,'cellid'],
                df_BSC2_LAC.loc[i,'修改后_LAC']                
)
        f.write(line+'\n') 

with open(data_path + 'FIX_REG-ZONE_BSC2.txt','w') as f:
    for i in range(0,len(df_BSC2),1):
        line = 'SET 1X_CELLSYSPARA:POS="{0}"-"{1}",REG_ZONE={2};'\
        .format(df_BSC2.loc[i,'system'],
                df_BSC2.loc[i,'cellid'],
                df_BSC2.loc[i,'修改后_REG_ZONE']               
)
        f.write(line+'\n') 

with open(data_path  +  'Release_right_BSC2.txt','w') as f:
    line_list = []
    for i in range(0,len(df_BSC2),1):
        line = 'RELEASE CMRIGHT:SYSTEM={0};'\
        .format(df_BSC2.loc[i,'system'])
        line_list.append(line)
    line_list = list(set(line_list))   
    for line in  line_list:
        f.write(line+'\n')         

