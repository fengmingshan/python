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
def ping_test(init_list,sleeptime):
    fault_set = set()
    for i in range(0,len(init_list),1):        
        tn = telnetlib.Telnet(host='6.48.255.24',port=23, timeout=5)     # 连接telnet服务器    
        tn.read_until(b'login:',timeout=3)   # 登录
        tn.write(b'qujing\n')      
        tn.read_until(b'password:',timeout=3)  # 登录
        tn.write(b'qjjk@2017\n' )
        if (init_list[i]+1)*92<len(command_list):
            for j in range(init_list[i]*92,(init_list[i]+1)*92,1):
                tn.write(command_list[j].encode('ascii') + b'\n')       # 输入ping命令 
        elif (i+1)*92 > len(command_list):
            for j in range(init_list[i]*92,len(command_list),1):
                tn.write(command_list[j].encode('ascii') + b'\n')       # 输入ping命令                 
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
    return fault_set

    
def task():
    sche.enter(1800,1,task)  # 调用sche实例的enter方法创建一个定时任务，1800秒之后执行，任务内容执行task()函数
    current_time = str(datetime.now()).split('.')[0]
    print('任务开始时间:',current_time)   # print任务开始时间
    t0 = datetime.now()
    global command_list
    random.shuffle(command_list)
    init_list = list(range(0,11,1))
    return_set = ping_test(init_list,sleeptime)    #以list[0,1,2..9]启动测试，如果失败，返回一个失败列表
    return_list = list(return_set)
    t1 = datetime.now()
    if len(return_list) > 0:
        new_sleeptime = sleeptime + 90
        if (t1-t0).seconds <1320:  # 计算程序运行时间，如果小于25分钟，则重测测试失败的部分 
            ping_test(return_list,new_sleeptime)   # 调用ping_test 函数再测一遍测试失败的部分 
    
    current_time = str(datetime.now()).split('.')[0]
    print('任务结束时间：',current_time)
    
# =============================================================================
# 汇总处理ping测试数据
# =============================================================================
    def get_time_info(record_file):
        time_array = record_file[:-9]
        time_info = time_array.replace('.',':') 
        return time_info
    
    all_files = os.listdir(data_path)
    file_list = []
    df_break = pd.DataFrame(columns=('eNodeB','基站名称','网管名称','IP','状态','断站时间','持续时长(分)','恢复时间','数据更新时间'))
    df_total = pd.DataFrame(columns=('IP','状态','数据更新时间'))
    
    today = datetime.today()
    yestoday =  today - timedelta(days=1)
    today = str(today).split(' ')[0] 
    yestoday = str(yestoday).split(' ')[0] 
    for file in all_files:
        if '_测试结果' in file:
            if get_time_info(file).split(' ')[0] == today or get_time_info(file).split(' ')[0] == yestoday:
                file_list.append(file)
            
    if len(file_list) > 0:    # 如果取到的文件列表不为空，则开始处理文件     
        for record_file in file_list:
            F= open(data_path + record_file,'r',encoding='utf-8')
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
            df_total_tmp2 = pd.DataFrame(columns=('IP','状态','数据更新时间'))
            for i in range(0,len(success_record),1):
                df_total_tmp.loc[i,'IP'] = success_record[i]
                df_total_tmp.loc[i,'状态'] = '正常'
                df_total_tmp.loc[i,'数据更新时间'] = get_time_info(record_file)    
            df_total = df_total.append(df_total_tmp,ignore_index=True)
            for i in range(0,len(break_record),1):
                df_total_tmp2.loc[i,'IP'] = break_record[i]
                df_total_tmp2.loc[i,'状态'] = '断站'
                df_total_tmp2.loc[i,'数据更新时间'] = get_time_info(record_file)
            df_total = df_total.append(df_total_tmp2,ignore_index=True)
            
        df_total = df_total.sort_values(by='数据更新时间',ascending = True)    
            
        df_break_bts = df_total[df_total['状态'] == '断站']
        break_bts = list(set(list(df_break_bts['IP'])))  # 通过set去重复，取出所有断站的基站IP的list
          
        for i in range(0,len(break_bts),1):
            df_tmp = df_total[df_total['IP'] == break_bts[i]]  # 筛选该基站的全部记录，包含正常的记录
            df_tmp = df_tmp.reset_index()
            break_list = []
            resume_list = []
            start_time = df_tmp.loc[0,'数据更新时间']
            end_time = df_tmp.loc[len(df_tmp)-1,'数据更新时间']   # 取最后一条记录时间为end_time
            if '正常' not in list(df_tmp['状态']):   # 如果记录里都是断站，则断站开始时间等于第一条记录时间
                break_list.append(start_time)
            elif df_tmp.loc[0,'状态'] =='断站':     # 如果第一条就是断站，则使用后面的前后关联方法无法提取出来，所以单独提取断站时间
                break_list.append(start_time)
                
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
        
            df_break_tmp = pd.DataFrame(columns=('eNodeB','基站名称','IP','状态','断站时间','持续时长(分)','恢复时间','数据更新时间'))
            for j in range(0,len(break_list),1):
                df_break_tmp.loc[j,'IP'] = df_tmp.loc[0,'IP']
                df_break_tmp.loc[j,'状态'] = '断站'
                df_break_tmp.loc[j,'断站时间'] = break_list[j]
                df_break_tmp.loc[j,'数据更新时间'] = end_time
                df_break_tmp = df_break_tmp.fillna('-')
                if len(resume_list) > j:
                    df_break_tmp.loc[j,'恢复时间'] = resume_list[j]
                if df_break_tmp.loc[j,'断站时间'] == '-':
                    df_break_tmp.loc[j,'持续时长(分)'] = (time.mktime(time.strptime(df_break_tmp.loc[j,'恢复时间'],'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(start_time,'%Y-%m-%d %H:%M:%S')))/60
                elif df_break_tmp.loc[j,'恢复时间'] == '-':
                    df_break_tmp.loc[j,'持续时长(分)'] = (time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_break_tmp.loc[j,'断站时间'],'%Y-%m-%d %H:%M:%S')))/60
                else:
                    df_break_tmp.loc[j,'持续时长(分)'] = (time.mktime(time.strptime(df_break_tmp.loc[j,'恢复时间'],'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_break_tmp.loc[j,'断站时间'],'%Y-%m-%d %H:%M:%S')))/60
            df_break =  df_break.append(df_break_tmp,ignore_index=True)
        
        
        df_break['IP'] = df_break['IP'].map(lambda x:x.replace('\n',''))
        df_break = pd.merge(df_break,df_bts,how='left',on='IP')
        df_break['eNodeB'] = df_break['eNBId']
        df_break['基站名称'] = df_break['Site Name(Chinese)']
        df_break['网管名称'] = df_break['Site Name']
        del df_break['eNBId']
        del df_break['Site Name(Chinese)']
        del df_break['Site Name']
        df_break = df_break[['eNodeB','基站名称','网管名称','IP','状态','断站时间','持续时长(分)','恢复时间','数据更新时间']]
    
        current_time = str(datetime.now()).split('.')[0]
        current_time = current_time.replace(':','.')       
        with pd.ExcelWriter(out_path + current_time + '_断站.xls') as writer:
            df_break.to_excel(writer,current_time + '_断站') 
            #df_total.to_excel(writer,'原始数据') 
        
        print('报表生成时间：',current_time)
        print('-----------------------------')

# =============================================================================
# 延时10秒后启动任务
# =============================================================================
sche.enter(12,1,task)  # 调用sche实力的enter方法创建一个定时任务，12秒之后执行，任务内容执行task()函数

print('task will run in 10 second') # 提示信息 10秒计时
for i in range(1,11,1):
    print('----->',i)
    time.sleep(1)
sche.run()


