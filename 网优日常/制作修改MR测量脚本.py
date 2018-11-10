# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:41:30 2018

@author: Administrator
"""
import pandas as pd
import os
from datetime import datetime 
current_date = str(datetime.now()).split('.')[0].split(' ')[0]

path = r'D:\MR报表' + '\\'
data_path =  r'D:\MR报表\需修改TOP小区' + '\\'
out_path = r'D:\MR报表\修改脚本' + '\\'
CELL_info = 'CELL_info_LC.xlsx'
df_CELL_info = pd.read_excel(path + CELL_info,dtype =str,encoding='utf-8')

top_files = os.listdir(data_path)
df_top = pd.DataFrame()
for file in top_files:
    df_tmp = pd.read_excel(data_path + file,encoding='utf-8')
    df_top = df_top.append(df_tmp)
df_top = df_top[['区域','NAME']]
df_top = pd.merge(df_top,df_CELL_info,how ='left',on = 'NAME' )  

df_OMMB1 =  df_top[df_top['OMMB']=='OMMB1']
df_OMMB1 =  df_OMMB1.reset_index()  

df_OMMB2 =  df_top[df_top['OMMB']=='OMMB2']
df_OMMB2 =  df_OMMB2.reset_index()  

with open(out_path + current_date+ '_' +  'FIX_top_cell_OMMB1.txt','w') as f:
    for i in range(0,len(df_OMMB1),1):
        line = r'UPDATE:MOC="EUtranCellMeasurement",MOI="{0}",ATTRIBUTES="intraFPeriodMeasSwitch=0",EXTENDS="";'\
        .format(df_OMMB1.loc[i,'MOI'])
        f.write(line+'\n')         
   
with open(out_path + 'Apply_right_top_OMMB1.txt','w') as f:
    for i in range(0,len(df_OMMB1),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_OMMB1.loc[i,'SubNetwork'],
                df_OMMB1.loc[i,'MEID']
)
        f.write(line+'\n') 

with open(out_path + current_date + '_' +  'FIX_top_cell_OMMB2.txt','w') as f:
    for i in range(0,len(df_OMMB2),1):
        line = r'UPDATE:MOC="EUtranCellMeasurement",MOI="{0}",ATTRIBUTES="intraFPeriodMeasSwitch=0",EXTENDS="";'\
        .format(df_OMMB2.loc[i,'MOI'])
        f.write(line+'\n')         
   
with open(out_path  + 'Apply_right_top_OMMB2.txt','w') as f:
    for i in range(0,len(df_OMMB2),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_OMMB2.loc[i,'SubNetwork'],
                df_OMMB2.loc[i,'MEID']
)
        f.write(line+'\n') 

#with  pd.ExcelWriter(path + 'df_top.xlsx')  as writer:  #输出到excel
    #df_top.to_excel(writer, 'df_top') 
       
        
