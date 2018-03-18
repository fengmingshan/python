# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 17:42:00 2018
按天汇总基站电压数据
@author: Administrator
"""

import os
import pandas as pd 
import time

voltage_path =r'D:\4G_voltage'+ '\\'
omm1_bts_name = 'omm1_bts_name.xls'
omm2_bts_name = 'omm2_bts_name.xls'


vo_files = os.listdir(voltage_path)

vo_file_list = []
for vofile in vo_files:
    if 'export-' in vofile:
            vo_file_list.append(vofile)  # 找出目录中所有电压采集文件
            
df_voltage_omm1 = pd.read_excel(voltage_path + omm1_bts_name,encoding='utf-8')
df_voltage_omm1['基站代码'] = df_voltage_omm1['基站代码'].astype(int)   
df_voltage_omm2 = pd.read_excel(voltage_path + omm2_bts_name,encoding='utf-8')
df_voltage_omm2['基站代码'] = df_voltage_omm2['基站代码'].astype(int) 
df_omm1_eNodeB = pd.DataFrame()
df_omm1_eNodeB['基站代码'] = df_voltage_omm1['基站代码']
df_omm2_eNodeB = pd.DataFrame()
df_omm2_eNodeB['基站代码'] = df_voltage_omm2['基站代码']

def get_time_array(file_name):    
    time_array = file_name[7:11]+'/'+ file_name[11:13]+'/'+ file_name[13:15]+' '\
    +  file_name[16:18] + ':' +  file_name[18:20] + ':' + file_name[20:22] 
    return time_array

def open_vofile(vo_file_list):  #定义打开原始记录文件的生成器函数
    for vofile in vo_file_list:  
        df_vofile = pd.read_csv(voltage_path + vofile,usecols=['网元','测试项','测试结果'],encoding='GBK') 
        yield df_vofile 

for vofile in vo_file_list:
    df_vofile = pd.read_csv(voltage_path + vofile,usecols=['网元','测试项','测试结果'],encoding='GBK') 
    df_vofile = df_vofile[df_vofile['测试项'].str.contains('输入电源电压')]
    df_vofile['测试结果'] = df_vofile['测试结果'].map(lambda x:x[:-1])
    df_vofile['测试结果'] = df_vofile['测试结果'].astype(float)
    del df_vofile['测试项']                    
    time_array =  get_time_array(vofile)

    if 'SubNetwork=530301,MEID=730318' in list(df_vofile['网元']):    #判断是OMM1还是OMM2    
        df_vofile['网元'] = df_vofile['网元'].map(lambda x:x.split('=')[2])
        df_vofile.rename(columns={'网元':'基站代码'}, inplace=True)
        df_vofile['基站代码'] = df_vofile['基站代码'].astype(int)   
        df_omm1_vo = pd.merge(df_omm1_eNodeB,df_vofile,how='left',on = '基站代码')
        df_voltage_omm1[time_array] = df_omm1_vo['测试结果']

    else:
        df_vofile['网元'] = df_vofile['网元'].map(lambda x:x.split('=')[2])
        df_vofile.rename(columns={'网元':'基站代码'}, inplace=True)
        df_vofile['基站代码'] = df_vofile['基站代码'].astype(int)   
        df_omm2_vo = pd.merge(df_omm2_eNodeB,df_vofile,how='left',on = '基站代码')    
        df_voltage_omm2[time_array] = df_omm2_vo['测试结果']

writer1 = pd.ExcelWriter(voltage_path + time_array[:10].replace('/','') + '_omm1.xls')
df_voltage_omm1.to_excel(writer1,'电压数据') 
writer1.save()

writer2 = pd.ExcelWriter(voltage_path + time_array[:10].replace('/','') + '_omm2.xls')
df_voltage_omm2.to_excel(writer2,'电压数据') 
writer2.save()
