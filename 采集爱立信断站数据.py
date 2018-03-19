# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 16:41:49 2018

@author: Administrator
"""

import pandas as pd
import telnetlib  
from telnetlib import Telnet
import socket
import pandas as pd
import time

path = 'd:\Eric'+'\\'
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
# 通过telnet ping测试基站
# =============================================================================
df_ip = pd.read_excel(path + bts , encoding='utf-8')
ip_list=list(df_ip['IP'])
command_list=list('ping '+x for x in ip_list)   # 生成ping命令

tn = telnetlib.Telnet(host = '6.48.255.24',port=23, timeout=30)     # 连接telnet服务器

tn.read_until(b'login:',timeout=5)   # 登录
tn.write(b'qujing\n')  

tn.read_until(b'password:',timeout=5)  # 登录
tn.write(b'qjjk@2017\n' )  

for command in command_list:   
    tn.write(command.encode('ascii') + b'\n')       # 输入ping命令

tn.write(b'exit'+b'\n')     # 退出telnet服务器     
time.sleep(2)
content = tn.read_all().decode('ascii')     # 保存ping测试结果
tn.close() 

current_time = get_current_time()
file_time = file_time.replace(':','.')
output= open(path + file_time + '原始数据.txt','a',encoding='utf-8')    # 将结果输出到文件夹
output.write(content)
output.close()

# =============================================================================
# 汇总处理ping测试数据
# =============================================================================
def get_time_info(record_file):
    time_array = record_file[:-4]
    time_info = time_array.replace('.',':') 
    return time_info

record_file = '2018-03-19 19.40.20.txt'
F= open(path + record_file,'r',encoding='utf-8')
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

df_total = pd.DataFrame(columns=('IP','状态','数据更新时间'))
df_break = pd.DataFrame(columns=('eNodeB','基站名称','IP','状态','断站时间','持续时长(分)','恢复时间','数据更新时间'))




for i in range(0,len(success_record),1):
    df_total.loc[i,'IP'] = success_record[i]
    df_total.loc[i,'状态'] = '正常'
    df_total.loc[i,'数据更新时间'] = get_time_info(record_file)

for i in range(0,len(break_record),1):
    df_total.loc[i,'IP'] = break_record[i]
    df_total.loc[i,'状态'] = '断站'
    df_total.loc[i,'数据更新时间'] = get_time_info(record_file)

df_total = df_total.sort_values(by='数据更新时间',ascending = True)    
df_break = df_total[df_total['状态'] == '断站']
break_list = list(set(list(df_break['IP'])))  # 通过set去重复，取出所有断站的基站IP的list
for i in range(0,len(break_list),1):
    df_tmp_break = df_total[(df_total['IP'] == break_list[i])&(df_total['状态'] == '断站')] # 逐个筛选断站的基站，找出所有断站记录
    df_tmp_break = df_tmp_break.reset_index()   # 重排序
    df_break[i,'IP'] = break_list[i]
    df_break.loc[i,'状态']=df_tmp_break.loc[0,'状态']
    df_break.loc[i,'断站时间']=df_tmp_break.loc[0,'数据更新时间']     # 取第一行记录的更新时间就是基站断站发生时间
    detal_time = (time.mktime(time.strptime(df_tmp_break.loc[len(df_tmp_break)-1,'数据更新时间'],'%Y-%m-%d %H:%M:%S')) - 
                  time.mktime(time.strptime(df_tmp_break.loc[0,'数据更新时间'],'%Y-%m-%d %H:%M:%S')))/60 #计算断站时长
    df_break.loc[i,'持续时长(分)']=detal_time    # 取最后一行断站记录时间和第一行记录的更新时间的差就是基站断站持续时间
    df_tmp_all = df_total[df_total['IP'] == break_list[i]]  # 筛选该基站的全部记录，包含正常的记录
    df_tmp_all = df_tmp_all.reset_index()
    for j in range(0,len(df_tmp_all)-1,1):
        if df_tmp_all.loc[j,'状态'] == '断站' and df_tmp_all.loc[j+1,'状态'] == '正常': # 如果'断站'后面有一行正常状态'正常'则表示故障恢复
            df_break.loc[i,'恢复时间'] = df_tmp_all.loc[j+1,'数据更新时间']    # 取最后一行断站记录时间和第一行记录的更新时间的差就是基站断站持续时间








with open(path+'断站.txt','a',encoding='utf-8') as output:
    for line in break_result:
        output.write(line+'\n')
output.close()