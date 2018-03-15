# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 08:43:04 2018

@author: Administrator
"""
import os
import pandas as pd
import time

#==============================================================================
# 获取当前日期
#==============================================================================
data_array=time.ctime(time.time()) # 获取当前时间
today = data_array[4:7]+'-'+data_array[8:10]  # 获取当前日期 格式为‘Mar-14’
sheet_time = data_array[11:13]+'点'+ data_array[14:16]+'分' # 获取表格生成的时间
data_trans = {'Jan':'1月','Feb':'2月','Mar':'3月','Apr':'4月','May':'5月','June':'6月',
              'July':'7月','Aug':'8月','Sept':'9月','Oct':'10月','Nov':'11月','Dec':'12月'} # 中英文月份对照字典
month = data_trans[today[0:3]]  # 将月份翻译为中文 
month_day = month + today[4:6]+'日'  # 构建当天日期格式为 '3月14日'


#==============================================================================
# 处理SCTP状态数据
#==============================================================================
data_path = r'd:\2018年工作\2018年LTE断站管控\sctp_data'+'\\'
out_path = r'd:\2018年工作\2018年LTE断站管控'+'\\'
eNodeB_name='eNode_name.xls'
df_eNodeB_name = pd.read_excel(data_path +eNodeB_name ,dtype =str,encoding='utf-8') 

all_files = os.listdir(data_path) 
file_list=[]
for file in all_files:
    if '2018-' in file:
        if file[5:11] == today:
            file_list.append(file)  # 找出今天采集的所有文件
if len(file_list) > 1:
    df_state=pd.DataFrame(columns=('eNodeB','基站名称','状态','更新时间')) # 新建表格用于存放基站状态汇总数据
    df_result=pd.DataFrame(columns=('eNodeB','基站名称','状态','发生时间','持续时间（分钟）','恢复时间')) #创建表格用于存放断站数据
    
    for file_name in file_list:
        updata_time = file_name[12:20].replace('-',':') # 通过原始文件名获取数据采集的时间
        file_tmp = open(data_path + file_name,'r',encoding='gbk')  # 用零时文件读取原始记录文件
        content = file_tmp.readlines() 
        df_state_tmp=pd.DataFrame(columns=('eNodeB','基站名称','状态','更新时间')) # 新建零时表格用于存放打开的原始记录
        for i in range(0,len(content),1):
            if 'NE=' in  content[i]:
                eNodeB = content[i].split(',')[1][3:9]
                state = content[i+4].split('      ')[2]
                state = state.replace(' ','')
                df_state_tmp.loc[i,'eNodeB']= eNodeB  # 将原始记录读入 df_state_tmp
                df_state_tmp.loc[i,'状态']= state
                df_state_tmp.loc[i,'更新时间']= updata_time
        df_state=df_state.append(df_state_tmp,ignore_index=True)  # 将 df_state_tmp加入到汇总表格 df_state   
    df_state = df_state.reset_index()   
    df_state=df_state.drop('index',axis=1)    
    df_state = pd.merge(df_state,df_eNodeB_name,how='left',on='eNodeB')
    df_state['基站名称']=df_state['网元名称']
    df_state =df_state.drop('网元名称',axis=1)
    
    df_break = df_state[df_state['状态'] == '链路断开。---'] #筛选出所有发生郭断站的基站
    break_set=set(list(df_break['eNodeB'])) # 断站基站去重复
    break_list = list(break_set)  # 得到去重后的断站list
    
    
    for i in range(0,len(break_list),1):
        df_tmp1=df_state[(df_state['eNodeB'] == break_list[i])&(df_state['状态'] == '链路断开。---')] # 逐个筛选断站基站，找出断站开始时间
        df_tmp1=df_tmp1.sort_values(by='更新时间',ascending = True) # 按时间顺序升序排列
        df_tmp1=df_tmp1.reset_index()
        df_result.loc[i,'eNodeB']=df_tmp1.loc[0,'eNodeB']
        df_result.loc[i,'基站名称']=df_tmp1.loc[0,'基站名称']
        df_result.loc[i,'状态']=df_tmp1.loc[0,'状态']
        df_result.loc[i,'发生时间']=df_tmp1.loc[0,'更新时间'] #取第一行记录就是基站断站发生时间
        hour = int(df_tmp1.loc[len(df_tmp1)-1,'更新时间'][0:2]) - int(df_tmp1.loc[0,'更新时间'][0:2])
        minute = int(df_tmp1.loc[len(df_tmp1)-1,'更新时间'][3:5]) - int(df_tmp1.loc[0,'更新时间'][3:5])
        df_result.loc[i,'持续时间（分钟）']= hour * 60 + minute # 计算基站中断持续的时间
        df_tmp2=df_state[df_state['eNodeB'] == break_list[i]] # 逐个筛选出发生过断站的基站，包含已恢复的
        df_tmp2=df_tmp2.sort_values(by='更新时间',ascending = True) # 按时间顺序升序排列
        df_tmp2=df_tmp2.reset_index()
        for j in range(0,len(df_tmp2)-1,1):
            if df_tmp2.loc[j,'状态'] == '链路断开。---' and df_tmp2.loc[j+1,'状态'] == '---': # 如果链路断开后面有一行正常状态‘---’则表示故障恢复
                df_result.loc[i,'恢复时间']= df_tmp2.loc[j+1,'更新时间'] 
            
    df_result = pd.merge(df_result,df_eNodeB_name,how='left',on='eNodeB')
    df_result['基站名称'] = df_result['网元名称'] 
    df_result['基站名称'] = df_result.drop('网元名称',axis=1)
    
    writer = pd.ExcelWriter(data_path + month_day + sheet_time + '基站断站及停电.xls')
    df_result.to_excel(writer,sheet_time + '_断站') 
    #df_state.to_excel(writer,sheet_time + '_原始数据') 
    writer.save()


        