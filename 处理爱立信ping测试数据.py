# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 16:41:49 2018

@author: Administrator
"""

import pandas as pd
import telnetlib  
import time
import os 

data_path = 'd:\Eric'+'\\'
bts = 'bts_list.xls'
# =============================================================================
# 获取当前时间信息
# =============================================================================
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



# =============================================================================
# 汇总处理ping测试数据
# =============================================================================
def get_time_info(record_file):
    time_array = record_file[:-9]
    time_info = time_array.replace('.',':') 
    return time_info

all_files = os.listdir(data_path)
file_list = []
df_break = pd.DataFrame(columns=('eNodeB','基站名称','IP','状态','断站时间','持续时长(分)','恢复时间'))
df_total = pd.DataFrame(columns=('IP','状态','数据更新时间'))

for file in all_files:
    if '测试结果' in file:
        file_list.append(file)
        
for record_file in file_list:
    with open(data_path + record_file,'r',encoding='utf-8') as F:
        lines = F.readlines()
        success_record=[]
        break_record=[]
        for line in lines:
            if 'is alive' in line:
                success_record.append(line)
            elif 'no answer from' in line:
                break_record.append(line)
            
    success_record = list(x.replace(' is alive','') for x in success_record)
    break_record = list(x.replace('no answer from ','') for x in break_record)    
    df_total_tmp = pd.DataFrame(columns=('IP','状态','数据更新时间'))
    for i in range(0,len(success_record),1):
        df_total_tmp.loc[i,'IP'] = success_record[i]
        df_total_tmp.loc[i,'状态'] = '正常'
        df_total_tmp.loc[i,'数据更新时间'] = get_time_info(record_file)    
    df_total = df_total.append(df_total_tmp,ignore_index=True)
    for i in range(0,len(break_record),1):
        df_total_tmp.loc[i,'IP'] = break_record[i]
        df_total_tmp.loc[i,'状态'] = '断站'
        df_total_tmp.loc[i,'数据更新时间'] = get_time_info(record_file)
    df_total = df_total.append(df_total_tmp,ignore_index=True)

df_total = df_total.sort_values(by='数据更新时间',ascending = True)    
    
df_break_bts = df_total[df_total['状态'] == '断站']
break_bts = list(set(list(df_break_bts['IP'])))  # 通过set去重复，取出所有断站的基站IP的list

for i in range(0,len(break_bts),1):
    df_tmp = df_total[df_total['IP'] == break_bts[i]]  # 筛选该基站的全部记录，包含正常的记录
    df_tmp = df_tmp.reset_index()
    break_list = []
    resume_list = []
    start_time = df_tmp.loc[0,'数据更新时间']
    end_time = df_tmp.loc[len(df_tmp)-1,'数据更新时间']
    if '正常' not in list(df_tmp['状态']):   # 如果记录里都是断站，则断站开始时间等于第一条记录时间
        break_list.append(start_time)
    else:
        for j in range(0,len(df_tmp)-1,1):
            if df_tmp.loc[j,'状态'] == '断站' and df_tmp.loc[j+1,'状态'] == '正常': # 如果'断站'后面有一行正常状态'正常'则表示故障恢复
                resume_list.append(df_tmp.loc[j+1,'数据更新时间'])    # 取最后一行断站记录时间和第一行记录的更新时间的差就是基站断站持续时间    
            elif df_tmp.loc[j,'状态'] == '正常' and df_tmp.loc[j+1,'状态'] == '断站': # 如果'正常'后面有一行正常状态'断站'则表示发生断站
                break_list.append(df_tmp.loc[j+1,'数据更新时间'])    # 取最后一行断站记录时间和第一行记录的更新时间的差就是基站断站持续时间
        if len(break_list) == 0 and len(resume_list) == 0 :
            break_list.append(df_tmp.loc[0,'数据更新时间'])   # 如果断站时间和恢复时间都是空，说明记录里全是断站记录，则取第一条作为断站发生时间
        elif len(break_list) == 0 and len(resume_list) == 1 :     
            break_list.insert(0,df_tmp.loc[0,'数据更新时间'])   # 如果只有恢复时间没有断站时间,则说明只发生了一次断站，则取第一条记录时间作为断站发生时间  
        elif len(break_list) > 0 and len(resume_list)> 0: 
            if time.strptime(resume_list[0],'%Y-%m-%d %H:%M:%S') < time.strptime(break_list[0],'%Y-%m-%d %H:%M:%S'):  
                break_list.insert(0,start_time)     #如果第一条恢复时间早于第一条断站时间，则说明还有一次断站发生在更早的时间，取开始时间作为断站时间
            elif time.strptime(break_list[len(break_list)-1],'%Y-%m-%d %H:%M:%S') > time.strptime(resume_list[len(resume_list)-1],'%Y-%m-%d %H:%M:%S') : 
                pass

    df_break_tmp = pd.DataFrame(columns=('eNodeB','基站名称','IP','状态','断站时间','持续时长(分)','恢复时间'))
    for j in range(0,len(break_list),1):
        df_break_tmp.loc[j,'IP'] = df_tmp.loc[0,'IP']
        df_break_tmp.loc[j,'状态'] = '断站'
        df_break_tmp.loc[j,'断站时间'] = break_list[j]
        df_break_tmp = df_break_tmp.fillna('-')
        if len(resume_list) != 0:
            df_break_tmp.loc[j,'恢复时间'] = resume_list[j]
        if df_break_tmp.loc[j,'断站时间'] == '-':
            df_break_tmp.loc[j,'持续时长(分)'] = (time.mktime(time.strptime(df_break_tmp.loc[j,'恢复时间'],'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(start_time,'%Y-%m-%d %H:%M:%S')))/60
        elif df_break_tmp.loc[j,'恢复时间'] == '-':
            df_break_tmp.loc[j,'持续时长(分)'] = (time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_break_tmp.loc[j,'断站时间'],'%Y-%m-%d %H:%M:%S')))/60
        else:
            df_break_tmp.loc[j,'持续时长(分)'] = (time.mktime(time.strptime(df_break_tmp.loc[j,'恢复时间'],'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_break_tmp.loc[j,'断站时间'],'%Y-%m-%d %H:%M:%S')))/60
    df_break =  df_break.append(df_break_tmp,ignore_index=True)


df_bts=pd.read_excel(data_path + bts,dtype =str,encoding='utf-8') 
df_break['IP'] = df_break['IP'].map(lambda x:x.replace('\n',''))
df_break = pd.merge(df_break,df_bts,how='left',on='IP')
df_break['eNodeB'] = df_break['eNBId']
df_break['基站名称'] = df_break['Site Name(Chinese)']
del df_break['eNBId']
del df_break['Site Name(Chinese)']

current_time = get_current_time() 
current_time = current_time.replace(':','.')       
writer = pd.ExcelWriter(data_path + current_time + '_断站.xls')
df_break.to_excel(writer,current_time + '_断站') 
df_total.to_excel(writer,'原始数据') 
writer.save()
