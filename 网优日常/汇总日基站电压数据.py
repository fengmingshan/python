# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 09:46:12 2018

@author: Administrator
"""
import pandas as pd
import numpy as np

import os 

data_path = r'D:\4G电压动态报表\2018年10月份电压值' + '\\'    #把一个月的电压汇总表放在这里
out_path = r'D:\4G电压动态报表' + '\\'              #汇总后的表格会输出到这里

file_list = os.listdir(data_path)
new_file = []
new_file_name = []

for file in file_list :
    df_tmp = pd.read_excel(data_path + file)
    df_tmp = df_tmp.dropna(how='all',axis = 1)
    old_columns = list(df_tmp.columns)
    for col in  old_columns:
        df_tmp[col] = df_tmp[col].map(lambda x:np.NaN if x == '-' else x )
        if '时间' in col :
            df_tmp[col] = df_tmp[col].fillna(method = 'pad' )                           
            df_tmp[col] = df_tmp[col].fillna(method = 'bfill' )
            df_tmp[col] = df_tmp[col].map(lambda x:x.split(' ')[1][0:5])
            
    voltage_columns = []
    other_columns = []
    for col in  old_columns:       
        if  '电压' not in col:
            other_columns.append(col)        
    for col in  old_columns:       
        if '电压' in col:
            voltage_columns.append(col)
    df_voltage = df_tmp[voltage_columns]
    df_other = df_tmp[other_columns]
    df_voltage = df_voltage.fillna(method = 'pad',axis = 1)
    df_voltage = df_voltage.fillna(method = 'bfill',axis = 1)
    df_tmp = df_other.join(df_voltage)
    df_tmp = df_tmp.reindex(columns = old_columns)
    new_file.append(df_tmp)
    new_file_name.append(file)

with  pd.ExcelWriter(out_path + '电压数据汇总.xlsx')  as writer:  #输出到excel
    for i in range(0,len(new_file),1):
        new_file[i].to_excel(writer,new_file_name[i].split('-')[2][0:2],index=None)

        
    
    
    
     