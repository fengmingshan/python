# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 16:41:49 2018

@author: Administrator
"""

import sched # 导入定时任务库
import time # 导入time模块
from datetime import datetime 
from datetime import timedelta 

import os
import telnetlib  
from telnetlib import Telnet
import socket 
import pandas as pd
import random

sche=sched.scheduler(time.time,time.sleep)  # 实例化sched.scheduler类
# =============================================================================
# 设置环境变量
# =============================================================================
data_path = 'E:\采集爱立信基站状态'+'\\'
out_path = 'F:\爱立信基站断站数据'+'\\'
bts = 'bts_list.xls'
sleeptime = 90  # 每一批测试命令中间的延时

df_bts = pd.read_excel(data_path + bts , encoding='utf-8')  # 打开基站名称表

ip_list=list(df_bts['IP'])
command_list = list('ping '+ x for x in ip_list)   # 生成ping命令列表

# =============================================================================
# 通过telnet ping测试基站
# =============================================================================
fault_set = set() 
command_line = 'display currentconfig'   
tn = telnetlib.Telnet(host='6.48.255.24',port=23, timeout=5)     # 连接telnet服务器    
tn.read_until(b'login:',timeout=3)   # 登录
tn.write(b'qujing\n')      
tn.read_until(b'password:',timeout=3)  # 登录
tn.write(b'qjjk@2017\n' )
tn.write(command_line.encode('ascii') + b'\n')       # 输入ping命令 
    # 输入ping命令                 
tn.write(b'exit'+b'\n')     # 退出telnet服务器 
time.sleep(sleeptime)    
#content = tn.set_debuglevel(10000)
#content = tn.read_all().decode('ascii')  # 保存测试结果
try:
    content = tn.read_all().decode('ascii') # 保存测试结果
    tn.close()   
    current_time = str(datetime.now()).split('.')[0]
    current_time = current_time.replace(':','.')
    with open(data_path + current_time + '_测试结果.txt','a',encoding='utf-8')  as output:  # 将结果输出到文件夹
        output.write(content)
except socket.timeout:
    fault_set.add(init_list[i])


    
def task():
    sche.enter(300,1,task)  # 调用sche实例的enter方法创建一个定时任务，300秒之后执行，任务内容执行task()函数
    return_set = ping_test(init_list,sleeptime)    #以list[0,1,2..9]启动测试，如果失败，返回一个失败列表
    
sche.enter(10,1,task)
