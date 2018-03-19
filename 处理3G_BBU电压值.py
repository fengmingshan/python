# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 17:13:59 2018

@author: Administrator
"""
import pandas as pd
import os

data_path=r'D:\电压曲线'+'\\' 
file_name='曲靖BSS1_2018-03-05_165636-fm-envi-info.txt'
file=data_path + file_name
df_result=[]

df_content = pd.read_table(file,sep='\t',header=0,index_col=None,engine='python')  
col_name=df_content.columns.map(lambda x:x.strip())
df_content.columns=col_name
df_content['BTS类型']=df_content['BTS类型'].map(lambda x:x.strip())
df_content=df_content[(df_content['BTS类型']!='CBTS I2')&(df_content['BTS类型']!='BTSB I4')]                                                  

df_tmp=df_content[['系统号','BTS类型','别名','输入电压(V)','更新时间']]
df_result.append(df_tmp)