# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 10:41:21 2018

@author: Administrator
"""
import pyautogui # 
import sched # 导入定时任务库
import time # 导入time模块
from datetime import datetime
from datetime import timedelta
import os
import shutil
import pandas as pd
import random

sche=sched.scheduler(time.time,time.sleep)  # 实例化sched.scheduler类

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1.5  # 停顿2秒
pyautogui.size()
width, height = pyautogui.size()

#==============================================================================
# 设置环境变量
#==============================================================================
data_path = r'F:\4G_SCTP_Voltage_data'+'\\'
out_path = r'F:\_中兴4G网管断站与停电'+'\\'
bak_path = r'F:\SCTP_Voltage_data_备份' + '\\'
cmd_path = r'C:\Users\Administrator' + '\\'
eNodeB_name='eNode_name.xls'
df_eNodeB_name = pd.read_excel(data_path + eNodeB_name ,dtype =str,encoding='utf-8') 
df_eNodeB_name['eNodeB'] =df_eNodeB_name['eNodeB'].astype(int)

# =============================================================================
# 定义数据采集和汇算任务
# =============================================================================
def task():
    sche.enter(1800,1,task)  # 调用sche实力的enter方法创建一个定时任务，1800秒之后执行，任务内容执行task()函数
    current_time = str(datetime.today()).split('.')[0]
    print('任务开始时间:',current_time)

    pyautogui.hotkey('winleft', 'd')    # 返回桌面
    time.sleep(1)
                
    # =============================================================================
    # 拆分诊断测试命令
    # =============================================================================
    vol_cmd_ommb1 = 'CMD_OMMB1.txt'
    SCTP_cmd_ommb1 = '查询SCTP脚本_ommb1.txt'
    
    vol_cmd_ommb2 = 'CMD_OMMB2.txt'
    SCTP_cmd_ommb2 = '查询SCTP脚本_ommb2.txt'
    
    # 拆分OMMB1的诊断测试脚本                    
    with open(cmd_path + vol_cmd_ommb1,encoding ='utf-8' ) as vol_file:
        vol_lines = vol_file.readlines()
        random.shuffle(vol_lines)   # 对电压诊断命令洗牌
    
    with open(cmd_path + SCTP_cmd_ommb1,encoding ='utf-8' ) as sctp_file:
        sctp_lines = sctp_file.readlines()
        random.shuffle(sctp_lines)  # 对sctp诊断命令洗牌
   
    for i in range(0,int(len(sctp_lines)/105) + 1,1):
        with open(cmd_path + 'B1CMD' + str(i+1) + '.txt','w',encoding ='utf-8' ) as f:
            if i <  int(len(sctp_lines)/105) :
                for j in range(i*105,(i+1)*105,1):
                    f.write(vol_lines[j]) 
                    f.write(sctp_lines[j]) 
            else:
                for j in range(i*105,len(vol_lines),1):
                    f.write(vol_lines[j]) 
                for k in range(i*105,len(sctp_lines),1):
                    f.write(sctp_lines[k]) 

    # 拆分OMMB2的诊断测试脚本                    
    with open(cmd_path + vol_cmd_ommb2,encoding ='utf-8' ) as vol_file:
        vol_lines = vol_file.readlines()
        random.shuffle(vol_lines)   # 对电压诊断命令洗牌
   
    with open(cmd_path + SCTP_cmd_ommb2,encoding ='utf-8' ) as sctp_file:
        sctp_lines = sctp_file.readlines()
        random.shuffle(sctp_lines)  # 对sctp诊断命令洗牌

    for i in range(0,int(len(sctp_lines)/114) + 1,1):
        with open(cmd_path + 'B2CMD' + str(i+1) + '.txt','w',encoding ='utf-8' ) as f:
            if i <  int(len(sctp_lines)/114) :
                for j in range(i*114,(i+1)*114,1):
                    f.write(vol_lines[j]) 
                    f.write(sctp_lines[j]) 
            else:
                for j in range(i*114,len(vol_lines),1):
                    f.write(vol_lines[j]) 
                for k in range(i*114,len(sctp_lines),1):
                    f.write(sctp_lines[k]) 
                        
    # =============================================================================
    #  获取诊断测试脚本   
    # =============================================================================
    cmd_files = os.listdir(cmd_path) 
    ommb1_cmd = []
    ommb2_cmd = []
    for file in cmd_files:
        if 'B1CMD' in file:            
            ommb1_cmd.append(file)
        elif  'B2CMD' in file:   
            ommb2_cmd.append(file)
    # =============================================================================
    # 诊断OMMB1
    # =============================================================================
    for i in range(0,3,1):
        bsc = os.popen(r'E:\netnumen\ems\ums-client\client.exe')
        bsc.close()
        time.sleep(3)
    
        pyautogui.moveTo(649,480, duration=0.5)   # 找到密码窗
        pyautogui.click()     # 点击
        
        pyautogui.typewrite('Fms123456!',0.7)  # 输入密码
    
        pyautogui.moveTo(809,557, duration=0.5)   # 找到登录按钮
        pyautogui.click()     # 登录BSC客户端
        time.sleep(5)
        pyautogui.hotkey('altleft', 'y')
        
        pyautogui.moveTo(700,300, duration=10)   # 慢慢移动到屏幕中间等待网管加载
    
        pyautogui.hotkey('altleft', 'c')
        time.sleep(1)
        pyautogui.hotkey('altleft', 'o')
        time.sleep(1)
        pyautogui.hotkey('altleft', 'm')
        time.sleep(1)
       
        pyautogui.moveTo(484,101, duration=5)   # 找到批处理标签
        pyautogui.click()     # 点击
        
        pyautogui.moveTo(705,145, duration=0.5)   # 找到选择网元
        pyautogui.click()     # 点击
        
        pyautogui.moveTo(506,217, duration=0.5)   # 选择OMMB1
        pyautogui.click()     # 点击
        
        pyautogui.moveTo(678,402, duration=0.5)   # 找到确定
        pyautogui.click()     # 点击
        
        for j in range (0,4,1):            
            pyautogui.moveTo(835,146, duration=0.5)   # 找到导入脚本按钮
            pyautogui.click()     # 点击
            
            pyautogui.moveTo(626,513, duration=0.5)   # 找到文件名框
            pyautogui.click()     # 点击
            
            pyautogui.typewrite(ommb1_cmd[i*4+j],0.4)  # 输入文件名
            pyautogui.press('enter')
            pyautogui.hotkey('altleft', 'O') # 打开文件
            
            pyautogui.moveTo(731,145, duration=0.5)   # 找到运行按钮
            pyautogui.click()     # 点击
            
            pyautogui.moveTo(685,495, duration=0.5)   # 找到确认执行按钮
            pyautogui.click()     # 点击
        
            pyautogui.moveTo(700,300, duration=0.5)   # 移动到中间，画框，等待任务结束
            time.sleep(45)   # 
        
        pyautogui.moveTo(1412,8, duration=0.5)   # 找到关闭BSC客户端按钮
        pyautogui.click()     # 点击
        time.sleep(3)   # 
        pyautogui.hotkey('altleft', 'y')
        
    # =============================================================================
    # 诊断OMMB2
    # =============================================================================
    for i in range(0,2,1):
        bsc = os.popen(r'E:\netnumen\ems\ums-client\client.exe')
        bsc.close()
        time.sleep(3)
    
        pyautogui.moveTo(649,480, duration=0.5)   # 找到密码窗
        pyautogui.click()     # 点击
        
        pyautogui.typewrite('Fms123456!',0.7)  # 输入密码
    
        pyautogui.moveTo(809,557, duration=0.5)   # 找到登录按钮
        pyautogui.click()     # 登录BSC客户端
        time.sleep(5)
        pyautogui.hotkey('altleft', 'y')
        
        pyautogui.moveTo(700,300, duration=10)   # 慢慢移动到屏幕中间等待网管加载
    
        pyautogui.hotkey('altleft', 'c')
        time.sleep(1)
        pyautogui.hotkey('altleft', 'o')
        time.sleep(1)
        pyautogui.hotkey('altleft', 'm')
        time.sleep(1)
       
        pyautogui.moveTo(484,101, duration=5)   # 找到批处理标签
        pyautogui.click()     # 点击
        
        pyautogui.moveTo(705,145, duration=0.5)   # 找到选择网元
        pyautogui.click()     # 点击
        
        pyautogui.moveTo(507,240, duration=0.5)   # 选择OMMB2
        pyautogui.click()     # 点击
        
        pyautogui.moveTo(678,402, duration=0.5)   # 找到确定
        pyautogui.click()     # 点击
        
        for j in range (0,4,1):            
            pyautogui.moveTo(835,146, duration=0.5)   # 找到导入脚本按钮
            pyautogui.click()     # 点击
            
            pyautogui.moveTo(626,513, duration=0.5)   # 找到文件名框
            pyautogui.click()     # 点击
            
            pyautogui.typewrite(ommb2_cmd[i*4+j],0.4)  # 输入文件名
            pyautogui.press('enter')
            pyautogui.hotkey('altleft', 'O') # 打开文件
            
            pyautogui.moveTo(731,145, duration=0.5)   # 找到运行按钮
            pyautogui.click()     # 点击
            
            pyautogui.moveTo(685,495, duration=0.5)   # 找到确认执行按钮
            pyautogui.click()     # 点击
        
            pyautogui.moveTo(700,300, duration=0.5)   # 移动到中间，画框，等待任务结束
            time.sleep(45)   # 
        
        pyautogui.moveTo(1412,8, duration=0.5)   # 找到关闭BSC客户端按钮
        pyautogui.click()     # 点击
        time.sleep(3)   # 
        pyautogui.hotkey('altleft', 'y')
    
    current_time = str(datetime.now()).split('.')[0]
    print('任务结束时间:',current_time)
    
    # =============================================================================
    # 原始文件采集和转储
    # =============================================================================
        
    all_files = os.listdir(data_path) 
    file_list = []      # 需要备份的电压数据
    file_delete = []    # 需要删除的系统记录数据
    for file in all_files:
        if 'QJ_OMMB' in file: # 找出当前采集的所有记录文件
            file_list.append(file)  
        elif '-系统命令-' in file:      #  找出不需要系统命令记录
            file_delete.append(file) 

    for file_del in file_delete:    #  删除不需要系统命令记录文件
        os.remove(data_path + file_del)
    
    for copyfile in file_list:
        shutil.copy(data_path + copyfile, bak_path)     #将文件备份到bakpath 
    current_time =str(datetime.now()).split('.')[0]
    print(current_time + ' '+ '数据入库完成：本次入库 %d 个文件!' % len(file_list))
    
    for deletefile in file_list: 
        os.remove(data_path + deletefile)   # 备份完成后，删除源文件
    
    # =============================================================================
    # 处理SCTP状态数据
    # =============================================================================
    today = datetime.today()
    yestoday = today - timedelta(days = 1)
    today = str(today).split(' ')[0]
    yestoday = str(yestoday).split(' ')[0]
    
    def get_data_info(file):    # 定义从文件中获取日期信息的函数
        data_array = file.split('-')[3]
        time_array1 = file.split('-')[4]
        time_array2 = file.split('-')[5]
        time_info =  data_array[0:4] + '-' + data_array[4:6] + '-' + data_array[6:] + ' ' + time_array1[0:2]+ ':' + time_array1[2:] + ':' + time_array2[0:2]
        return time_info

    calc_file = []
    bak_files = os.listdir(bak_path) 
    for file in bak_files:
        if 'QJ_OMMB' in file:
            if (get_data_info(file).split(' ')[0] == today or 
                get_data_info(file).split(' ')[0] == yestoday):
                calc_file.append(file)
    
    if len(calc_file) > 1:
        df_state=pd.DataFrame(columns=('eNodeB','基站名称','状态','更新时间')) # 新建表格用于存放基站状态汇总数据
        df_result=pd.DataFrame(columns=('eNodeB','基站名称','状态','发生时间','持续时间（分钟）','恢复时间','数据更新时间')) #创建表格用于存放断站数据    
        for file_name in calc_file:
            updata_time = get_data_info(file_name)  # 通过原始文件名获取数据采集的时间
            with open(bak_path + file_name,'r',encoding='gbk') as file_tmp:  # 用零时文件读取原始记录文件
                content = file_tmp.readlines() 
                df_state_tmp=pd.DataFrame(columns=('eNodeB','基站名称','状态','更新时间')) # 新建零时表格用于存放打开的原始记录
                for i in range(0,len(content)-2,1) :
                    if 'NE=' in  content[i] and '运行状态' in  content[i+2]:
                        eNodeB = content[i].split(',')[1][3:9]
                        state = content[i+4].split('    ')[2]
                        state = state.replace(' ','')
                        df_state_tmp.loc[i,'eNodeB']= eNodeB  # 将原始记录写 df_state_tmp
                        df_state_tmp.loc[i,'状态']= state
                        df_state_tmp.loc[i,'更新时间']= updata_time
                df_state=df_state.append(df_state_tmp,ignore_index=True)  # 将 df_state_tmp加入到汇总表格 df_state   
        df_state = df_state.reset_index()   
        df_state=df_state.drop('index',axis=1) 
        df_state['状态']=df_state['状态'].map(lambda x:x.replace('链路断开。---','断站'))
        df_state['状态']=df_state['状态'].map(lambda x:x.replace('处理超时。---','断站'))
        df_state['状态']=df_state['状态'].map(lambda x:x.replace('---','正常'))
        df_state['eNodeB']=df_state['eNodeB'].astype(int)
        df_state = pd.merge(df_state,df_eNodeB_name,how='left',on='eNodeB')
        df_state['基站名称']=df_state['网元名称']
        df_state =df_state.drop('网元名称',axis=1)
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
                if df_result_tmp.loc[k,'恢复时间'] != '-':    
                    df_result_tmp.loc[k,'持续时间（分钟）']= (time.mktime(time.strptime(df_result_tmp.loc[k,'恢复时间'],'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_result_tmp.loc[k,'发生时间'],'%Y-%m-%d %H:%M:%S')))/60 # 计算基站中断持续的时间
                else:
                    df_result_tmp.loc[k,'持续时间（分钟）']= (time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_result_tmp.loc[k,'发生时间'],'%Y-%m-%d %H:%M:%S')))/60 # 计算基站中断持续的时间
    
            df_result = df_result.append(df_result_tmp,ignore_index=True)
    
        df_result = pd.merge(df_result,df_eNodeB_name,how='left',on='eNodeB')
        df_result['基站名称'] = df_result['网元名称'] 
        df_result = df_result.drop('网元名称',axis=1)
    
    # =============================================================================
    # 处理电压数据                  
    # =============================================================================    
    df_vol=pd.DataFrame(columns=['基站名称','区县','eNodeB','直流电压','采集时间'])     # 用于装电压原始数据
    df_power_down = pd.DataFrame(columns=['基站名称','区县','eNodeB','当前电压',
            '市电状态','停电时间','持续时间','恢复时间','数据更新时间'])  # 停电基站表，用于装停电基站
    
    if len(calc_file) > 0:
        for vofile_name in calc_file:        
            collect_time = get_data_info(vofile_name)  # 通过文件名提取时间信息
            with open(bak_path + vofile_name,'r',encoding='gbk') as file_tmp1:  # 用零时文件读取原始记录文件
                content = file_tmp1.readlines() 
                df_tmp1=pd.DataFrame(columns=['基站名称','区县','eNodeB','直流电压','采集时间'])
                for i in range(0,len(content)-5,1):
                    if 'NE=' in  content[i] and 'PM单板诊断测试' in  content[i+5]:
                        df_tmp1.loc[i,'eNodeB']= content[i].split(',')[1][3:]
                        df_tmp1.loc[i,'采集时间']= collect_time
                        df_tmp1.loc[i,'直流电压']= float(content[i+5].split('    ')[3].split(' ')[4][:-1])
                df_tmp1 = df_tmp1.groupby(by='eNodeB',as_index=False)[['基站名称','区县','直流电压','采集时间']].max()
                if len(df_tmp1)>0:
                    df_vol = df_vol.append(df_tmp1,ignore_index=True)  
        df_vol['eNodeB'] = df_vol['eNodeB'].astype(int)
        df_vol = pd.merge(df_vol,df_eNodeB_name,how = 'left',on = 'eNodeB')
        df_vol['基站名称'] = df_vol['网元名称']
        df_vol['区县']=df_vol['基站名称'].map(lambda x:x.split('_')[1][2:4])
        df_vol = df_vol.sort_values(by='采集时间',ascending = True)
        df_vol=df_vol.reset_index()
        del df_vol['网元名称']
        del df_vol['index']
        
        
        df_low_power = df_vol[df_vol['直流电压']<50]     # 筛选电池电压低于50v的基站，可能发生了停电
        low_power_bts =  list(set(list(df_low_power['eNodeB']))) #通过转换为set去重复
        for i in range(0,len(low_power_bts),1):        
            df_btsvol = df_vol[df_vol['eNodeB'] == low_power_bts[i]]
            df_btsvol = df_btsvol.reset_index()
            df_btsvol['市电状态'] = ''
            if len(df_btsvol)>=2:
                if df_btsvol.loc[len(df_btsvol)-1,'直流电压'] -df_btsvol.loc[len(df_btsvol)-2,'直流电压'] <= -0.3:   #计算电压差，最后一行需要单独计算
                    df_btsvol.loc[len(df_btsvol)-1,'市电状态'] = '停电'
                elif df_btsvol.loc[len(df_btsvol)-1,'直流电压'] -df_btsvol.loc[len(df_btsvol)-2,'直流电压'] >= 0.3: 
                    df_btsvol.loc[len(df_btsvol)-1,'市电状态'] = '来电'
    
            for j in range(1,len(df_btsvol)-1,1):
                if df_btsvol.loc[j,'直流电压'] - df_btsvol.loc[j+1,'直流电压'] >= 0.3:      # 循环计算电压差，得到市电状态
                    df_btsvol.loc[j,'市电状态'] = '停电'
                elif df_btsvol.loc[j,'直流电压'] - df_btsvol.loc[j+1,'直流电压'] <= -0.3:
                    df_btsvol.loc[j,'市电状态'] = '来电'
        
            df_down_tmp = pd.DataFrame(columns=['基站名称','区县','eNodeB','当前电压',
            '市电状态','停电时间','持续时间','恢复时间','数据更新时间'])
            start_time = df_btsvol.loc[0,'采集时间']  
            end_time = df_btsvol.loc[len(df_btsvol)-1,'采集时间']     
            break_time = [] # 用来存储停电时间
            resume_time = [] # 用来存储恢复时间
            if df_btsvol.loc[0,'市电状态'] =='停电':
                break_time.append(start_time)
            for k in range(0,len(df_btsvol)-1,1):
                if df_btsvol.loc[k,'市电状态'] =='' and df_btsvol.loc[k+1,'市电状态'] =='停电' and df_btsvol.loc[k+1,'直流电压'] < 53.5 :
                    break_time.append(df_btsvol.loc[k+1,'采集时间'])
                elif df_btsvol.loc[k,'市电状态'] =='来电' and df_btsvol.loc[k+1,'市电状态'] =='停电' and df_btsvol.loc[k+1,'直流电压'] < 53.5 :
                    break_time.append(df_btsvol.loc[k+1,'采集时间'])
                elif df_btsvol.loc[k,'市电状态'] =='' and df_btsvol.loc[k+1,'市电状态'] =='来电' and df_btsvol.loc[k+1,'直流电压'] <53.5:
                    resume_time.append(df_btsvol.loc[k+1,'采集时间'])
                elif df_btsvol.loc[k,'市电状态'] =='停电' and df_btsvol.loc[k+1,'市电状态'] =='来电' and df_btsvol.loc[k+1,'直流电压'] <53.5:
                    resume_time.append(df_btsvol.loc[k+1,'采集时间'])
            
            if len(break_time) == 0 and  len(resume_time) > 0:
                break_time.append(start_time)     # 如果break_time没有值，则说明停电发生在更早的时间，则视为发生在start_time
            elif len(break_time) > 1 and  len(resume_time) == 0:
                break_time = [break_time[0]]    #如果有多条停电时间没有恢复时间，则说明停电一直没有恢复，则只需保留第一条停电记录就行了
            elif len(break_time) > 0 and  len(resume_time) > 0:
                lis_tmp=[] 
                break_time_copy = break_time[:]
                for k in range(0,len(break_time_copy),1) :
                    if time.strptime(break_time_copy[k],'%Y-%m-%d %H:%M:%S') > time.strptime(resume_time[len(resume_time)-1],'%Y-%m-%d %H:%M:%S'):
                        lis_tmp.append(break_time_copy[k])  # 找出时间晚于最后一次恢复时间的所有停电，可以视为都是一次停电
                if len(lis_tmp) > 1:
                    for m in range(1,len(lis_tmp),1):
                        break_time.remove(lis_tmp[m]) # 保留最早的一条，其余可视为重复记录删除                        
                if time.strptime(break_time[0],'%Y-%m-%d %H:%M:%S') > time.strptime(resume_time[0],'%Y-%m-%d %H:%M:%S'):
                    resume_time.pop(0)  #如果第一次停电时间比第一次恢复时间还晚，则说明停电时间发生在更早，则第一次恢复时间无意思，删除        
            if len(break_time) > 1 and  len(resume_time) > 0:
                break_time_copy = break_time[:]
                resume_time_copy = resume_time[:]
                #对停电时间去重
                for k in range(1,len(break_time_copy),1):
                    if  break_time_copy[k] < resume_time_copy[0]:  #找出所有时间早于第一次恢复时间的停电，除第一条
                        break_time.remove(break_time_copy[k])    # 全部删除。因为都是同一次停电，        

            if len(break_time) > 1 and  len(resume_time) > 1:
                for k in range(1,len(resume_time),1):
                    lis_tmp=[] 
                    for l in range(1,len(break_time),1):
                        if ( time.strptime(resume_time[k-1] ,'%Y-%m-%d %H:%M:%S')<
                            time.strptime(break_time[l] ,'%Y-%m-%d %H:%M:%S') < 
                            time.strptime(resume_time[k] ,'%Y-%m-%d %H:%M:%S')):
                            lis_tmp.append(break_time[l]) 
                    for m in range(1,len(lis_tmp),1):
                        if  lis_tmp[m] in break_time:
                            break_time.remove(lis_tmp[m])
            
                #对恢复时间去重
                for k in range(1,len(break_time),1):
                    lis_tmp=[] 
                    for l in range(0,len(resume_time),1):
                        if ( time.strptime(break_time[k-1] ,'%Y-%m-%d %H:%M:%S')<
                            time.strptime(resume_time[l] ,'%Y-%m-%d %H:%M:%S') < 
                            time.strptime(break_time[k] ,'%Y-%m-%d %H:%M:%S')):
                            lis_tmp.append(resume_time[l]) 
                    for m in range(1,len(lis_tmp),1):
                        if  lis_tmp[m] in resume_time:
                            resume_time.remove(lis_tmp[m])
            
            for n in range(0,len(break_time),1):
                df_down_tmp.loc[n,'基站名称'] = df_btsvol.loc[0,'基站名称']
                df_down_tmp.loc[n,'区县'] = df_btsvol.loc[0,'基站名称'].split('QJ')[1][0:2]
                df_down_tmp.loc[n,'eNodeB'] = df_btsvol.loc[0,'eNodeB']
                df_down_tmp.loc[n,'当前电压'] = df_btsvol.loc[len(df_btsvol)-1,'直流电压']
                df_down_tmp.loc[n,'数据更新时间'] = end_time
            
                if len(break_time)-1 >= n:
                    df_down_tmp.loc[n,'市电状态'] = '停电'
                    df_down_tmp.loc[n,'停电时间'] = break_time[n]
                if len(resume_time)-1 >= n:
                    df_down_tmp.loc[n,'恢复时间'] = resume_time[n]
                df_down_tmp = df_down_tmp.fillna('-')
                if df_down_tmp.loc[n,'停电时间'] != '-' and  df_down_tmp.loc[n,'恢复时间'] == '-':
                    df_down_tmp.loc[n,'持续时间'] = (time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_down_tmp.loc[n,'停电时间'],'%Y-%m-%d %H:%M:%S')))/60
                elif  df_down_tmp.loc[n,'停电时间'] != '-' and  df_down_tmp.loc[n,'恢复时间'] != '-':
                    df_down_tmp.loc[n,'持续时间'] = (time.mktime(time.strptime(df_down_tmp.loc[n,'恢复时间'],'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(df_down_tmp.loc[n,'停电时间'],'%Y-%m-%d %H:%M:%S')))/60
            df_power_down = df_power_down.append(df_down_tmp,ignore_index=True)
            
        df_power_down['持续时间'] = df_power_down['持续时间'].map(lambda x:round(x,0))  # 处理小数点位数
        
        current_time = str(datetime.now()).split('.')[0]
        print('报表完成时间:',current_time)
        print('---------------------------------')
        current_time = current_time.replace(':','.')
        
        with  pd.ExcelWriter(out_path + current_time + '_基站断站及停电.xls') as writer :
            df_result.to_excel(writer,current_time + '_断站') 
            df_power_down.to_excel(writer,current_time +'_停电') 
            #df_vol.to_excel(writer,current_time +'_电压原始数据') 
        


sche.enter(12,1,task)  # 调用sche实力的enter方法创建一个定时任务，12秒之后执行，任务内容执行task()函数

print('task will run in 10 second') # 提示信息 10秒计时
for i in range(1,11,1):
    print('----->',i)
    time.sleep(1)

sche.run()
   
    
    
    
    
    
    
    
