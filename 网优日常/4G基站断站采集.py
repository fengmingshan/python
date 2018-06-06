# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 16:12:56 2018

@author: Administrator
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 16:41:49 2018

@author: Administrator
"""

import sched # 导入定时任务库
import time # 导入time模块
from datetime import datetime 
from datetime import timedelta 
from cmd import Cmd

import os
import pandas as pd
import random

sche=sched.scheduler(time.time,time.sleep)  # 实例化sched.scheduler类
# =============================================================================
# 设置环境变量
# =============================================================================
data_path = 'd:\_4G基站断站'+'\\'
log_path = 'd:\_4G基站断站\logfiles'+'\\'
out_path = 'd_4G基站断站'+'\\'
bts = 'bts_list.xlsx'

df_bts = pd.read_excel(data_path + bts , encoding='utf-8')  # 打开基站名称表

# =============================================================================
# 通过cmd ping测试基站
# =============================================================================
def ping_test(df_bts):    

                
def task():
    sche.enter(1800,1,task)  # 调用sche实例的enter方法创建一个定时任务，1800秒之后执行，任务内容执行task()函数
    current_time = str(datetime.now()).split('.')[0]
    print('任务开始时间:',current_time)   # print任务开始时间
    ping_test(return_list,new_sleeptime)   # 调用ping_test 函数再测一遍测试失败的部分 
    
    current_time = str(datetime.now()).split('.')[0]
    current_time = current_time.replace(':','-')
    with open(log_path + current_time + '.txt','w',encoding = 'utf8') as f:  
        for i in range(0,len(df_bts)):
            ip = df_bts.loc[i,'IP']
            BTS = df_bts.loc[i,'name']
            eNodeB = df_bts.loc[i,'eNodeB']
            command_line = 'ping'+ ' ' + ip + ' '+ '-n 1'   # 生成ping命令列表
            res = os.popen(command_line).readlines()
            del(res[3])
            current_time = str(datetime.now()).split('.')[0]
            info = str(BTS) + ' ' + str(eNodeB) +' ' + str(ip) +' '+ 'Time:' + ' ' +current_time 
            f.write(info)
            for line in res: 
                f.write(line)
            f.write('\n')
    
    current_time = str(datetime.now()).split('.')[0]
    print('任务结束时间：',current_time)
    
# =============================================================================
# 汇总处理ping测试数据
# =============================================================================
    def get_time_info(record_file):
        time_array = record_file[:-9]
        time_info = time_array.replace('.',':') 
        return time_info
    
    all_files = os.listdir(log_path)
    file_list = []
    df_break = pd.DataFrame(columns=('eNodeB','基站名称','网管名称','IP','状态','断站时间','持续时长(分)','恢复时间','数据更新时间'))
    df_total = pd.DataFrame(columns=('IP','状态','数据更新时间'))
    
    today = datetime.today()
    yestoday =  today - timedelta(days=1)
    today = str(today).split(' ')[0] 
    yestoday = str(yestoday).split(' ')[0] 
    for file in all_files:
        if get_time_info(file).split(' ')[0] == today or get_time_info(file).split(' ')[0] == yestoday:
            file_list.append(file)
            
    if len(file_list) > 0:    # 如果取到的文件列表不为空，则开始处理文件     
        df_state=pd.DataFrame(columns=('eNodeB','基站名称','状态','更新时间')) # 新建表格用于存放基站状态汇总数据
        df_result=pd.DataFrame(columns=('eNodeB','基站名称','状态','发生时间','持续时间（分钟）','恢复时间','数据更新时间')) #创建表格用于存放断站数据    
        for file_name in file_list:
            with open(log_path + file_name,'r',encoding='utf-8') as file_tmp:  # 用零时文件读取原始记录文件
                content = file_tmp.readlines() 
                df_state_tmp=pd.DataFrame(columns=('eNodeB','基站名称','状态','更新时间')) # 新建零时表格用于存放打开的原始记录
                for i in range(0,len(content)-2,1) :
                    if 'Time' in  content[i]:
                        bts_name =  content[i].split(' ')[0]
                        eNodeB = content[i].split(' ')[1]
                        updata_time = content[i].split(' ')[4] + ' ' + content[i].split(' ')[5]
                        state = content[i+2].split(' ')[0]
                        df_state_tmp.loc[i,'eNodeB']= eNodeB  # 将原始记录写入df_state_tmp
                        df_state_tmp.loc[i,'基站名称']= bts_name  # 将原始记录写入df_state_tmp
                        df_state_tmp.loc[i,'状态']= state
                        df_state_tmp.loc[i,'更新时间']= updata_time.strip ()
                df_state=df_state.append(df_state_tmp,ignore_index=True)  # 将 df_state_tmp加入到汇总表格 df_state   
        df_state = df_state.reset_index()   
        df_state=df_state.drop('index',axis=1) 
        df_state['状态']=df_state['状态'].map(lambda x:x.replace('Request','断站'))
        df_state['状态']=df_state['状态'].map(lambda x:x.replace('Reply','正常'))
        df_state['eNodeB']=df_state['eNodeB'].astype(int)
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
            end_time = df_tmp.loc[len(df_tmp)-1,'更新时间']       # 取最后一条记录时间为end_time
            if '正常' not in list(df_tmp['状态']):  # 如果状态全是断站，则断站开始时间为第一条记录时间
                break_list.append(start_time)
            elif df_tmp.loc[0,'状态'] =='断站':     # 如果第一条就是断站，则使用后面的前后关联方法无法提取出来，所以单独提取断站时间
                break_list.append(start_time)
                
            for j in range(0,len(df_tmp)-1,1):
                if df_tmp.loc[j,'状态'] == '断站' and df_tmp.loc[j+1,'状态'] == '正常': # 如果断站后面有一行正常状态则表示故障恢复
                    resume_list.append(df_tmp.loc[j+1,'更新时间'])
                elif df_tmp.loc[j,'状态'] == '正常'  and df_tmp.loc[j+1,'状态'] == '断站': # 如果‘正常’后面有一行‘断站’则表示发生断站
                    break_list.append(df_tmp.loc[j+1,'更新时间'])
            
            if len(resume_list) == 0 and len(break_list) > 0:  # 表示发生过断站但一直没恢复，无需处理
                pass                
            elif len(break_list) > 0 and len(resume_list) > 0:
                if time.strptime(resume_list[0],'%Y-%m-%d %H:%M:%S') <  time.strptime(break_list[0],'%Y-%m-%d %H:%M:%S'):
                    break_list.insert(0, start_time)    # 如果恢复时间比断站时间还早则说明在更早的时候还有一次断站，断站时间为 start_time
            
            df_result_tmp = pd.DataFrame(columns=('eNodeB','基站名称','状态','发生时间','持续时间（分钟）','恢复时间','数据更新时间')) #创建表格用于存放断站数据    
            for k in range(0,len(break_list),1): 
                df_result_tmp.loc[k,'eNodeB']= df_tmp.loc[0,'eNodeB']
                df_result_tmp.loc[k,'基站名称']= df_tmp.loc[0,'基站名称']
                df_result_tmp.loc[k,'状态']='断站'
                df_result_tmp.loc[k,'发生时间']= break_list[k] 
                df_result_tmp.loc[k,'数据更新时间']= end_time

                if len(resume_list) > k:
                    df_result_tmp.loc[k,'恢复时间']= resume_list[k] 
                df_result_tmp = df_result_tmp.fillna('-')
                if df_result_tmp.loc[k,'恢复时间'] != '-'  :    
                    df_result_tmp.loc[k,'持续时间（分钟）']= (time.mktime(time.strptime(df_result_tmp.loc[k,'恢复时间'],'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_result_tmp.loc[k,'发生时间'],'%Y-%m-%d %H:%M:%S')))/60 # 计算基站中断持续的时间
                else:
                    df_result_tmp.loc[k,'持续时间（分钟）']= (time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_result_tmp.loc[k,'发生时间'],'%Y-%m-%d %H:%M:%S')))/60 # 计算基站中断持续的时间    
            df_result = df_result.append(df_result_tmp,ignore_index=True)
        
        current_time = str(datetime.now()).split('.')[0]
        print('报表完成时间:',current_time)
        print('---------------------------------')
        current_time = current_time.replace(':','.')

        with  pd.ExcelWriter(data_path + current_time + '_基站断站及停电.xls') as writer :
            df_result.to_excel(writer,current_time + '_断站') 

# =============================================================================
# 延时10秒后启动任务
# =============================================================================
sche.enter(12,1,task)  # 调用sche实力的enter方法创建一个定时任务，12秒之后执行，任务内容执行task()函数
print('task will run in 10 second') # 提示信息 10秒计时
for i in range(1,11,1):
    print('----->',i)
    time.sleep(1)
sche.run()
   

