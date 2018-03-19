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
data_array=time.ctime(time.time()) # 获取当前时间
today = data_array[4:7]+'-'+data_array[8:10]  # 获取当前日期 格式为‘Mar-14’
collect_time = data_array[11:13]+'点'+ data_array[14:16]+'分' # 获取报表生成的时间
data_trans = {'Jan':'1月','Feb':'2月','Mar':'3月','Apr':'4月','May':'5月','June':'6月',
              'July':'7月','Aug':'8月','Sept':'9月','Oct':'10月','Nov':'11月','Dec':'12月'} # 中英文月份对照字典
month = data_trans[today[0:3]]  # 将月份翻译为中文 
month_day = month + today[4:6]+'日'  # 构建当天日期格式为 '3月14日'


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

output= open(path + month_day + '_' + collect_time + '原始数据.txt','a',encoding='utf-8')    # 将结果输出到文件夹
output.write(content)
output.close()

# =============================================================================
# 汇总处理ping测试数据
# =============================================================================
def get_time_info(record_file):
    data_array=time.ctime(time.time()) # 获取当前时间
    year = data_array[-4:]
    month =  record_file.split('月')[0]
    if len(month) == 1:
        month = '0' + month
    day =  record_file.split('_')[0].split('月')[1][:-1]
    if len(day) == 1:
        day = '0' + day
  
    data = year + '/' + 


record_file = '3月19日_17点44分原始数据.txt'
F= open(path + record_file,'r',encoding='utf-8')
lines = F.readlines()
success_record=[]
break_record=[]

df_total = pd.DataFrame(columns=('IP','状态','数据更新时间'))
df_break = pd.DataFrame(columns=('eNodeB','基站名称','IP','状态','断站发生时间','恢复时间','数据更新时间'))


for line in lines:
    if 'is alive' in line:
        success_record.append(line)
    elif 'no answer from' in line:
        break_record.append(line)

for i in range(0,len(success_record),1):
    df_total.loc[i,'IP'] = success_record[i]
    df_total.loc[i,'状态'] = '正常'
    df_total.loc[i,'数据更新时间'] = record_file[6:12]

for i in range(0,len(break_record),1):
    df_total.loc[i,'IP'] = break_record[i]
    df_total.loc[i,'状态'] = '断站'
    df_total.loc[i,'数据更新时间'] = record_file[6:12]

    



with open(path+'断站.txt','a',encoding='utf-8') as output:
    for line in break_result:
        output.write(line+'\n')
output.close()