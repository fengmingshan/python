# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 16:32:20 2019

@author: Administrator
"""

import pandas as pd
import os
from datetime import datetime 
current_date = str(datetime.now()).split('.')[0].split(' ')[0]

data_path = r'D:\test' + '\\'

df_OMMB1 = pd.read_excel(data_path + 'EUtranCellMeasurement_OMMB1.xlsx',encoding='utf-8')
df_OMMB1 = df_OMMB1.drop(0)
df_OMMB1 = df_OMMB1.drop(1)
df_OMMB1 = df_OMMB1.drop(2)
df_OMMB1 =  df_OMMB1[df_OMMB1['intraFPeriodMeasSwitch'] == '0']
df_OMMB1 =  df_OMMB1.reset_index()  

df_OMMB2 = pd.read_excel(data_path + 'EUtranCellMeasurement_OMMB2.xlsx',encoding='utf-8')
df_OMMB2 = df_OMMB2.drop(0)
df_OMMB2 = df_OMMB2.drop(1)
df_OMMB2 = df_OMMB2.drop(2)
df_OMMB2 =  df_OMMB2[df_OMMB2['intraFPeriodMeasSwitch'] == '0']
df_OMMB2 =  df_OMMB2.reset_index()  

df_OMMB3 = pd.read_excel(data_path + 'EUtranCellMeasurement_OMMB3.xlsx',encoding='utf-8')
df_OMMB3 = df_OMMB3.drop(0)
df_OMMB3 = df_OMMB3.drop(1)
df_OMMB3 = df_OMMB3.drop(2)
df_OMMB3 =  df_OMMB3[df_OMMB3['intraFPeriodMeasSwitch'] == '0']
df_OMMB3 =  df_OMMB3.reset_index()  



with open(data_path + current_date+ '_' +  'Modify_MR_OMMB1.txt','w') as f:
    for i in range(0,len(df_OMMB1),1):
        line = r'UPDATE:MOC="EUtranCellMeasurement",MOI="{0}",ATTRIBUTES="intraFPeriodMeasSwitch=1",EXTENDS="";'\
        .format(df_OMMB1.loc[i,'MOI'])
        f.write(line+'\n')         

with open(data_path + 'Apply_right_MR_OMMB1.txt','w') as f:
    for i in range(0,len(df_OMMB1),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_OMMB1.loc[i,'SubNetwork'],
                df_OMMB1.loc[i,'MEID']
)
        f.write(line+'\n') 

with open(data_path + current_date + '_' +  'Modify_MR_OMMB2.txt','w') as f:
    for i in range(0,len(df_OMMB2),1):
        line = r'UPDATE:MOC="EUtranCellMeasurement",MOI="{0}",ATTRIBUTES="intraFPeriodMeasSwitch=1",EXTENDS="";'\
        .format(df_OMMB2.loc[i,'MOI'])
        f.write(line+'\n')         
   
with open(data_path  + 'Apply_right_MR_OMMB2.txt','w') as f:
    for i in range(0,len(df_OMMB2),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_OMMB2.loc[i,'SubNetwork'],
                df_OMMB2.loc[i,'MEID']
)
        f.write(line+'\n') 

with open(data_path + current_date + '_' +  'Modify_MR_OMMB3.txt','w') as f:
    for i in range(0,len(df_OMMB3),1):
        line = r'UPDATE:MOC="EUtranCellMeasurement",MOI="{0}",ATTRIBUTES="intraFPeriodMeasSwitch=1",EXTENDS="";'\
        .format(df_OMMB3.loc[i,'MOI'])
        f.write(line+'\n')         
   
with open(data_path  + 'Apply_right_MR_OMMB3.txt','w') as f:
    for i in range(0,len(df_OMMB3),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_OMMB3.loc[i,'SubNetwork'],
                df_OMMB3.loc[i,'MEID']
)
        f.write(line+'\n') 

#with  pd.ExcelWriter(path + 'df_top.xlsx')  as writer:  #输出到excel
    #df_top.to_excel(writer, 'df_top') 
       
        
