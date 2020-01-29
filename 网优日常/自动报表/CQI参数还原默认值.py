# -*- coding: utf-8 -*-
"""
Created on Fri May 10 17:11:46 2019

@author: Administrator
"""

import pandas as pd
import os
path = r'D:\test' + '\\'
file = r'D:\test\质差小区第二批.xls'

df_cell = pd.read_excel(file,encoding='utf-8')
df_cell['小区编码'] = df_cell['网元'].map(str) + '_' + df_cell['小区'].map(str)

config_files = [x for x in os.listdir(path) if 'PhyChannel' in x ]
df_PhyChannel = pd.DataFrame()
for file in config_files :
    df_tmp = pd.read_excel(path + file ,encoding='utf-8') 
    df_tmp = df_tmp.drop([0,1,2])
    df_tmp['OMMB'] = file.split('_')[1][0:5]
    df_PhyChannel = df_PhyChannel.append(df_tmp)
df_PhyChannel = df_PhyChannel[['OMMB','MOI','SubNetwork','MEID','description','cqiRptPeriod','cqiRptChNum',]]
df_PhyChannel['MOI'] = df_PhyChannel['MOI'].map(lambda x:x.replace('ConfigSet=0,',''))
df_PhyChannel['description'] = df_PhyChannel['description'].map(lambda x:x.split('=')[1])
df_PhyChannel['description'] = df_PhyChannel['MEID'] + '_' + df_PhyChannel['description']
df_PhyChannel.rename(columns={'description':'小区编码'},inplace =True)

df_cell = pd.merge(df_cell,df_PhyChannel,how = 'left' , on = '小区编码' )
df_cell = df_cell[df_cell['MOI'].isnull() == False]
df_cell = df_cell.reset_index()

with open(path + '_modify_CQI.txt','w') as f:
    for i in range(0,len(df_cell),1):
        line = r'UPDATE:MOC="PhyChannel",MOI="{0}",ATTRIBUTES="cqiRptPeriod=\"1;3;5\",cqiRptChNum=\"1;0;5\"",EXTENDS="";'\
        .format(df_cell.loc[i,'MOI'])
        f.write(line+'\n') 
    

with open(path + 'apply_right_eNode.txt','w') as f:
    for i in range(0,len(df_cell),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_cell.loc[i,'SubNetwork'],
                df_cell.loc[i,'MEID'],
)
        f.write(line+'\n')         
        
        