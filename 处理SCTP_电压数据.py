# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 08:43:04 2018

@author: Administrator
"""
import os
import pandas as pd
import time

from xlrd import open_workbook

data_path = r'd:\2018年工作\2018年LTE断站管控\sctp_data'+'\\'
all_files = os.listdir(data_path) 

data_array=time.ctime(time.time())
today = data_array[4:7]+'-'+data_array[8:10]
sheet_time = data_array[11:13]+'点'+ data_array[14:16]+'分' # 获取表格生成的时间
data_trans = {'Jan':'1月','Feb':'2月','Mar':'3月','Apr':'4月','May':'5月','June':'6月',
              'July':'7月','Aug':'8月','Sept':'9月','Oct':'10月','Nov':'11月','Dec':'12月'}
month = data_trans[today[0:3]]  #翻译月份
day = month + today[4:6]+'日'  # 构建当天日期

file_list=[]
for file in all_files:
    if file[5:11] == today:
        file_list.append(file)  # 找出今天采集的所有文件

df_state=pd.DataFrame(columns=('eNodeB','基站名称','状态','更新时间'))
df_state_tmp=pd.DataFrame(columns=('eNodeB','基站名称','状态','更新时间'))

df_result=pd.DataFrame(columns=('eNodeB','基站名称','状态','发生时间','持续时间（分钟）','恢复时间'))

for file_name in file_list:
    updata_time = file_name[12:20].replace('-',':')
    file_tmp = open(data_path + file_name,'r',encoding='gbk') 
    content = file_tmp.readlines()
    df_state_tmp=pd.DataFrame(columns=('eNodeB','基站名称','状态','更新时间'))
    for i in range(0,len(content),1):
        if 'NE=' in  content[i]:
            eNodeB = content[i].split(',')[1][3:9]
            state = content[i+4].split('      ')[2]
            state = state.replace(' ','')
            df_state_tmp.loc[i,'eNodeB']= eNodeB
            df_state_tmp.loc[i,'状态']= state
            df_state_tmp.loc[i,'更新时间']= updata_time
    df_state=df_state.append(df_state_tmp,ignore_index=True)           
df_state = df_state.reset_index()   
df_state=df_state.drop('index',axis=1)    
df_break = df_state[df_state['状态'] == '链路断开。---'] #筛选出所有发生郭断站的基站
break_set=set(list(df_break['eNodeB'])) # 断站基站去重复
break_list = list(break_set)  # 得到去重后的断站list

for i in range(0,len(break_tuple),1):
    df_tmp=df_state[(df_state['eNodeB'] == break_list[i])&(df_state['状态'] == '链路断开。---')] # 逐个筛选断站基站，找出断站开始时间
    df_tmp=df_tmp.sort_values(by='更新时间',ascending = True)
    df_tmp=df_tmp.reset_index()
    df_result.loc[i,'eNodeB']=df_tmp.loc[0,'eNodeB']
    df_result.loc[i,'基站名称']=df_tmp.loc[0,'基站名称']
    df_result.loc[i,'状态']=df_tmp.loc[0,'状态']
    df_result.loc[i,'发生时间']=df_tmp.loc[0,'更新时间']
    hour = int(df_tmp.loc[len(df_tmp)-1,'更新时间'][0:2]) - int(df_tmp.loc[0,'更新时间'][0:2])
    minute = int(df_tmp.loc[len(df_tmp)-1,'更新时间'][3:5]) - int(df_tmp.loc[0,'更新时间'][3:5])
    df_result.loc[i,'持续时间']= hour*60 + minute
    df_tmp=df_state[df_state['eNodeB'] == break_tuple[i]] # 逐个筛选出发生过断站的基站，包含已恢复的
    df_tmp=df_tmp.sort_values(by='更新时间',ascending = True)
    df_tmp=df_tmp.reset_index()
    if df_tmp.loc[len(df_tmp)-1,'状态'] == '---':
        df_result.loc[i,'恢复时间']= df_tmp.loc[len(df_tmp)-1,'更新时间']
    
writer = pd.ExcelWriter(data_path + day + '基站断站及停电.xls')
df_state.to_excel(writer,sheet_time + '_更新') 
df_result.to_excel(writer,sheet_time + '_断站') 
writer.save()


        