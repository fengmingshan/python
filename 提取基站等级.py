# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 16:22:15 2018

@author: Administrator
"""
import os
import sys
import pandas as pd

data_path = r'd:\2018年工作\_2018年小区退服时长管控\小区基础数据'
files=os.listdir(data_path)   
df_data=pd.DataFrame()
df_cell_num=pd.DataFrame(columns=[['区县','小区数量','AB类小区数量','CD类小区数量']])

for filename in files:
    if filename!=r'cell_num.xls' :
        file=data_path+'\\'+filename
        df_tmp=pd.read_excel(file,dtype =str,encoding='utf-8') 
        df_data=df_data.append(df_tmp,ignore_index=True)  
    
df_data['所属eNBID名称']=df_data['所属eNBID名称'].map(lambda x: x.replace('调测_',''))   # 将基站名称切片得到基站等级
df_data['所属eNBID名称']=df_data['所属eNBID名称'].map(lambda x: x.replace('调测-',''))   # 将基站名称切片得到基站等级
df_data['所属eNBID名称']=df_data['所属eNBID名称'].map(lambda x: x.replace('整治_',''))   # 将基站名称切片得到基站等级

for i in range(0,len(df_data),1):   
    df_data.loc[i,'CELL_ID']=df_data.loc[i,'小区名称'].split('_')[1]  # 将基站名称切片得到CELL_ID
    df_data.loc[i,'CELL_INDEX']=df_data.loc[i,'所属eNBID']+'_'+df_data.loc[i,'CELL_ID']# 将基站名称切片得到CELL_ID
    if df_data.loc[i,'小区等级']=='':
        df_data.loc[i,'小区等级']='C'
    
df_data=df_data.rename(columns={'区/市/县/旗':'区县'})
df_data['区县']=df_data['区县'].map(lambda x: x[:-1])
df_data=df_data[(df_data['CELL_ID'] != '81')&(df_data['CELL_ID']!= '82')&(df_data['CELL_ID']!= '83')
&(df_data['CELL_ID']!='209')&(df_data['CELL_ID']!='210')&(df_data['CELL_ID']!='211')
&(df_data['CELL_ID']!='212')&(df_data['CELL_ID']!='213')&(df_data['CELL_ID']!='214')] 


df_cell_list=df_data[['区县','CELL_INDEX','所属eNBID','CELL_ID','小区名称','小区等级']]
df_tmp=df_data[['区县','小区等级']]
df_sum=df_tmp.groupby(by='区县',as_index=False).count()
df_tmp1=df_tmp[(df_tmp['小区等级']=='A')|(df_tmp['小区等级']=='B')]
df_sum_AB=df_tmp1.groupby(by='区县',as_index=False).count()
df_tmp1=df_tmp[(df_tmp['小区等级']=='C')|(df_tmp['小区等级']=='D')]
df_sum_CD=df_tmp1.groupby(by='区县',as_index=False).count()
df_sum=pd.merge(df_sum,df_sum_AB,how='left',on='区县')
df_sum=pd.merge(df_sum,df_sum_CD,how='left',on='区县')
df_sum=df_sum.rename(columns={'小区等级_x':'小区数量','小区等级_y':'A/B类小区数量','小区等级':'C/D类小区数量'})

writer = pd.ExcelWriter(data_path+'\\'+'cell_num.xls') #输出到excel
df_sum.to_excel(writer, 'cell_num')
df_cell_list.to_excel(writer, 'cell_list')
#df_data.to_excel(writer, '原始数据')
writer.save()

