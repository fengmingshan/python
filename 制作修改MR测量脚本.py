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
config_files = [x for x in os.listdir(path) if 'Measurement' in x ]
df_CELL_info = pd.DataFrame()
for file in config_files:
    df_tmp = pd.read_excel(path + file,encoding='utf-8')
    df_tmp = df_tmp.drop([0,1,2],axis=0)
    df_tmp = df_tmp[['MOI','SubNetwork','MEID','description']]
    df_tmp['description'] = df_tmp['description'].map(lambda x:x.split('=')[1])
    df_tmp['cell_id'] = df_tmp['MEID'] + '_' + df_tmp['description']
    df_tmp['OMMB'] = file.split('_')[1][0:5]
    df_CELL_info = df_CELL_info.append(df_tmp)


top_files = os.listdir(data_path)
df_top = pd.DataFrame()
for file in top_files:
    df_tmp = pd.read_excel(data_path + file,encoding='utf-8')
    df_top = df_top.append(df_tmp)
df_top = df_top[['区域','NAME']]
df_top['eNB'] = df_top['NAME'].map(lambda x:x.split('_')[0])
df_top['cell'] = df_top['NAME'].map(lambda x:x.split('_')[1])
df_top['cell_id'] = df_top['eNB'] + '_' + df_top['cell']
df_top = pd.merge(df_top,df_CELL_info,how ='left',on = 'cell_id' )  

df_OMMB1 =  df_top[df_top['OMMB']=='OMMB1']
df_OMMB1 =  df_OMMB1.reset_index()  

df_OMMB2 =  df_top[df_top['OMMB']=='OMMB2']
df_OMMB2 =  df_OMMB2.reset_index()  

df_OMMB3 =  df_top[df_top['OMMB']=='OMMB3']
df_OMMB3 =  df_OMMB3.reset_index()  



with open(out_path + current_date+ '_' +  'Modify_MR_OMMB1.txt','w') as f:
    for i in range(0,len(df_OMMB1),1):
        line = r'UPDATE:MOC="EUtranCellMeasurement",MOI="{0}",ATTRIBUTES="intraFPeriodMeasSwitch=0",EXTENDS="";'\
        .format(df_OMMB1.loc[i,'MOI'])
        f.write(line+'\n')         
   
with open(out_path + 'Apply_right_MR_OMMB1.txt','w') as f:
    for i in range(0,len(df_OMMB1),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_OMMB1.loc[i,'SubNetwork'],
                df_OMMB1.loc[i,'MEID']
)
        f.write(line+'\n') 

with open(out_path + current_date + '_' +  'Modify_MR_OMMB2.txt','w') as f:
    for i in range(0,len(df_OMMB2),1):
        line = r'UPDATE:MOC="EUtranCellMeasurement",MOI="{0}",ATTRIBUTES="intraFPeriodMeasSwitch=0",EXTENDS="";'\
        .format(df_OMMB2.loc[i,'MOI'])
        f.write(line+'\n')         
   
with open(out_path  + 'Apply_right_MR_OMMB2.txt','w') as f:
    for i in range(0,len(df_OMMB2),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_OMMB2.loc[i,'SubNetwork'],
                df_OMMB2.loc[i,'MEID']
)
        f.write(line+'\n') 

with open(out_path + current_date + '_' +  'Modify_MR_OMMB3.txt','w') as f:
    for i in range(0,len(df_OMMB3),1):
        line = r'UPDATE:MOC="EUtranCellMeasurement",MOI="{0}",ATTRIBUTES="intraFPeriodMeasSwitch=0",EXTENDS="";'\
        .format(df_OMMB3.loc[i,'MOI'])
        f.write(line+'\n')         
   
with open(out_path  + 'Apply_right_MR_OMMB3.txt','w') as f:
    for i in range(0,len(df_OMMB3),1):
        line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
        .format(df_OMMB3.loc[i,'SubNetwork'],
                df_OMMB3.loc[i,'MEID']
)
        f.write(line+'\n') 

#with  pd.ExcelWriter(path + 'df_top.xlsx')  as writer:  #输出到excel
    #df_top.to_excel(writer, 'df_top') 
       
        
