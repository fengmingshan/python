# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 09:58:45 2018

@author: Administrator
"""
import os
import pandas as pd 
import time

data_path =r'D:\4G_voltage'+'\\'
file_list = os.listdir(data_path)
voltage_log='voltage_log.txt'
sctp_log='sctp_log.txt'

v_log = open(data_path+'\\'+voltage_log,'r',encoding='utf-8')
s_log = open(data_path+'\\'+sctp_log,'r',encoding='utf-8')

file_name ='export-20180308_161313.csv' 

t=file_name[7:15]+file_name[16:22] # 取出采集时间字符串
time_array=(int(t[0:4]),int(t[4:6]),int(t[6:8]),int(t[8:10]),int(t[10:12]),int(t[12:14]),5,50,1) # 转换采集时间为struct_time
collect_time=time.strftime('%Y/%m/%d %H:%M:%S',time_array) # 转换采集时间为正常时间格式

file = data_path + file_name
df_voltage=pd.DataFrame(columns=['网元名称','区县','基站代码','采集时间','直流电压'])
df_vol=pd.DataFrame(columns=['网元名称','区县','基站代码','采集时间','直流电压'])

df_sctp=pd.DataFrame(columns=['网元名称','区县','基站代码','采集时间','基站状态'])
df_break=pd.DataFrame(columns=['网元名称','区县','基站代码','采集时间','基站状态'])


df_tmp = pd.read_csv(file,encoding='GBK') 
df_tmp=df_tmp[df_tmp['测试项'].str.contains('输入电源电压')]

df_tmp['网元名称']=df_tmp['网元名称'].map(lambda x:x.replace('整治-',''))
df_tmp['网元名称']=df_tmp['网元名称'].map(lambda x:x.replace('整治_',''))
df_tmp['网元名称']=df_tmp['网元名称'].map(lambda x:x.replace('调测-',''))
df_tmp['网元名称']=df_tmp['网元名称'].map(lambda x:x.replace('调测_',''))


bts=list(df_tmp['网元名称'])
bts_set=set(bts)
bts_list=sorted(list(bts_set))
bts_list=[i.replace('整治-','') for i in bts_list]
bts_list=[i.replace('整治_','') for i in bts_list]
bts_list=[i.replace('调测_','') for i in bts_list]
bts_list=[i.replace('调测-','') for i in bts_list] 

for i in range(0,len(bts_list),1):
    df_voltage.loc[i,'网元名称']=bts_list[i]
    df_voltage.loc[i,'区县']=bts_list[i][9:11]

df_tmp1=pd.merge(df_voltage,df_tmp,how='left',on='网元名称')
df_voltage['基站代码']=df_tmp1['网元']
df_voltage['直流电压']=df_tmp1['测试结果']
df_voltage['采集时间']=collect_time
df_voltage['直流电压']=df_voltage['直流电压'].map(lambda x:float(x[:-1]))

df_vol=df_vol.append(df_voltage)
df_vol=df_vol.




