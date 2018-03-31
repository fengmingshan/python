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
def get_current_time():
    month_trans = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'June':6,
              'July':7,'Aug':8,'Sept':9,'Oct':10,'Nov':11,'Dec':12} # 中英文月份对照字典
    time_str = time.ctime(time.time())
    time_tuple = tuple(time.localtime())    
    year = int(time_str[-4:])
    month = month_trans[time_str.split(' ')[1]]  # 查月份翻译表得到数字的月份
    day = int(time_str.split(' ')[2])
    hour = int(time_str.split(' ')[3][0:2])
    minute = int(time_str.split(' ')[3][3:5])
    second = int(time_str.split(' ')[3][-2:])
    tm_wday = time_tuple[-3]    # 周几
    tm_yday = time_tuple[-2]    # 一年中的第几天
    tm_isdst = time_tuple[-1]    # 是否夏令时    
    struct_time = (year,month,day,hour,minute,second,tm_wday,tm_yday,tm_isdst)
    current_time = time.strftime('%Y-%m-%d %H:%M:%S',struct_time) # 转换采集时间为正常时间格式
    return current_time

#==============================================================================
# 处理SCTP状态数据
#==============================================================================
data_path = r'd:\SCTP'+'\\'
out_path = r'd:\SCTP'+'\\'
eNodeB_name='eNode_name.xls'
df_eNodeB_name = pd.read_excel(data_path +eNodeB_name ,dtype =str,encoding='utf-8') 

current_time = get_current_time()
today = current_time.split(' ')[0]

def get_data_info(file):    # 定义从文件中获取日期信息的函数
    data_array = file.split('-')[3]
    time_array1 = file.split('-')[4]
    time_array2 = file.split('-')[5]
    time_info =  data_array[0:4] + '-' + data_array[4:6] + '-' + data_array[6:] + ' ' + time_array1[0:2]+ ':' + time_array1[2:] + ':' + time_array2[0:2]
    return time_info


all_files = os.listdir(data_path) 
file_list = []
file_delete = [] 
for file in all_files:
    if '-云南曲靖电信LTE' in file: # 找出今天采集的所有记录文件
        if get_data_info(file).split(' ')[0] == today:
            file_list.append(file)  
    elif '-系统命令-' in file:      #  找出不需要系统命令记录
        file_delete.append(file) 
        
for file_del in file_delete:    #  删除不需要系统命令记录文件
    os.remove(file_del)

if len(file_list) > 1:
    df_state=pd.DataFrame(columns=('eNodeB','基站名称','状态','更新时间')) # 新建表格用于存放基站状态汇总数据
    df_result=pd.DataFrame(columns=('eNodeB','基站名称','状态','发生时间','持续时间（分钟）','恢复时间')) #创建表格用于存放断站数据    
    for file_name in file_list:
        updata_time = get_data_info(file_name)  # 通过原始文件名获取数据采集的时间
        file_tmp = open(data_path + file_name,'r',encoding='gbk')  # 用零时文件读取原始记录文件
        content = file_tmp.readlines() 
        df_state_tmp=pd.DataFrame(columns=('eNodeB','基站名称','状态','更新时间')) # 新建零时表格用于存放打开的原始记录
        for i in range(0,len(content),1):
            if 'NE=' in  content[i] and '运行状态' in  content[i+2]:
                eNodeB = content[i].split(',')[1][3:9]
                state = content[i+4].split('      ')[2]
                state = state.replace(' ','')
                df_state_tmp.loc[i,'eNodeB']= eNodeB  # 将原始记录写 df_state_tmp
                df_state_tmp.loc[i,'状态']= state
                df_state_tmp.loc[i,'更新时间']= updata_time
        df_state=df_state.append(df_state_tmp,ignore_index=True)  # 将 df_state_tmp加入到汇总表格 df_state   
    df_state = df_state.reset_index()   
    df_state=df_state.drop('index',axis=1) 
    df_state['状态']=df_state['状态'].map(lambda x:x.replace('链路断开。---','断站'))
    df_state['状态']=df_state['状态'].map(lambda x:x.replace('---','正常'))
    df_state = pd.merge(df_state,df_eNodeB_name,how='left',on='eNodeB')
    df_state['基站名称']=df_state['网元名称']
    df_state = df_state.drop('网元名称',axis=1)
    df_state = df_state.sort_values(by='更新时间',ascending = True) # 按时间顺序升序排列
    df_state = df_state.reset_index()
    del df_state['index']

    
    df_break = df_state[df_state['状态'] == '断站'] #筛选出所有发生郭断站的基站
    break_set=set(list(df_break['eNodeB'])) # 断站基站去重复
    break_bts = list(break_set)  # 得到去重后的断站list
        
    for i in range(0,len(break_bts),1):
        df_tmp = df_state[df_state['eNodeB'] == break_bts[i]] # 逐个筛选出发生过断站的基站，包含已恢复的
        df_tmp = df_tmp.reset_index()
        break_list = []
        resume_list = []
        start_time =  df_tmp.loc[0,'更新时间']      # 取第一条记录时间为start_time
        end_time = df_tmp.loc[len(df_tmp)-1,'更新时间']     # 取最后一条记录时间为end_time
        if '正常' not in list(df_tmp['状态']):  # 如果状态全是断站，则断站开始时间为第一条记录时间
            break_list.append(start_time)
        else:    
            for j in range(0,len(df_tmp)-1,1):
                if df_tmp.loc[j,'状态'] == '断站' and df_tmp.loc[j+1,'状态'] == '正常': # 如果断站后面有一行正常状态则表示故障恢复
                    resume_list.append(df_tmp.loc[j+1,'更新时间'])
                elif df_tmp.loc[j,'状态'] == '正常'  and df_tmp.loc[j+1,'状态'] == '断站': # 如果‘正常’后面有一行‘断站’则表示发生断站
                    break_list.append(df_tmp.loc[j+1,'更新时间'])
        if len(break_list) == 0 and len(resume_list) > 0:  # 表示从第一条记录开始就是断站，则断站时间一定是 start_time
            break_list.insert(0,start_time)
        elif len(resume_list) == 0 and len(break_list) > 0:  # 表示发生过断站但一直没恢复，无需处理
            pass                
        elif len(break_list) > 0 and len(resume_list) > 0:
            if time.strptime(resume_list[0],'%Y-%m-%d %H:%M:%S') <  time.strptime(break_list[0],'%Y-%m-%d %H:%M:%S'):
                break_list.insert(0,'start_time')    # 如果恢复时间比断站时间还早则说明在更早的时候还有一次断站，断站时间为 start_time
        
        df_result_tmp = pd.DataFrame(columns=('eNodeB','基站名称','状态','发生时间','持续时间（分钟）','恢复时间')) #创建表格用于存放断站数据    
        for k in range(0,len(break_list),1): 
            df_result_tmp.loc[k,'eNodeB']= df_tmp.loc[0,'eNodeB']
            df_result_tmp.loc[k,'基站名称']= df_tmp.loc[0,'基站名称']
            df_result_tmp.loc[k,'状态']='断站'
            df_result_tmp.loc[k,'发生时间']= break_list[k] 
            if len(resume_list) > k:
                df_result_tmp.loc[k,'恢复时间']= resume_list[k] 
            df_result_tmp = df_result_tmp.fillna('-')
            if df_result_tmp.loc[k,'恢复时间'] != '-':    
                df_result_tmp.loc[k,'持续时间（分钟）']= (time.mktime(time.strptime(df_result_tmp.loc[k,'恢复时间'],'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_result_tmp.loc[k,'发生时间'],'%Y-%m-%d %H:%M:%S')))/60 # 计算基站中断持续的时间
            else:
                df_result_tmp.loc[k,'持续时间（分钟）']= (time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_result_tmp.loc[k,'发生时间'],'%Y-%m-%d %H:%M:%S')))/60 # 计算基站中断持续的时间

        df_result = df_result.append(df_result_tmp,ignore_index=True)

    df_result = pd.merge(df_result,df_eNodeB_name,how='left',on='eNodeB')
    df_result['基站名称'] = df_result['网元名称'] 
    df_result = df_result.drop('网元名称',axis=1)
    
    current_time = get_current_time()
    current_time = current_time.replace(':','.')
    writer = pd.ExcelWriter(data_path + current_time + '基站断站及停电.xls')
    df_result.to_excel(writer,current_time + '_断站') 
    df_state.to_excel(writer,'原始数据') 
    writer.save()


        