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

sche=sched.scheduler(time.time,time.sleep)  # 实例化sched.scheduler类

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1.5  # 停顿2秒
pyautogui.size()
width, height = pyautogui.size()

today = datetime.today()    # 获取时间信息   
yestoday = today - timedelta(days = 1)
today = str(today).split(' ')[0]
yestoday = str(yestoday).split(' ')[0]

#==============================================================================
# 设置环境变量
#==============================================================================
data_path = r'D:\电压采集程序\data_path'+'\\'
bak_path = r'D:\电压采集程序\bak_path' + '\\'
out_path = r'D:\电压采集程序\report_path'+'\\'
eNodeB_name = 'eNode_name.xls'
OMMB1 =  'OMMB1.xls'
OMMB2 =  'OMMB2.xls'

# =============================================================================
# 定义采集电压的任务函数
# =============================================================================
def collect_task():
    sche.enter(1800,1,collect_task)  # 调用sche实力的enter方法创建一个定时任务，1800秒之后执行，任务内容执行task()函数
    current_time = str(datetime.now()).split('.')[0]
    print('任务开始时间:',current_time)   # 在cmd窗体中输出任务开始时间信息

    # =============================================================================
    # 登陆BSC    
    # =============================================================================
    pyautogui.hotkey('winleft', 'd')    # 返回桌面
    time.sleep(1)

    ommb = os.popen(r'D:\软件备份\netnumen\ems\ums-client\client.exe')
    ommb.close()    # 关闭cmd窗体

    pyautogui.moveTo(600,414, duration=0.5)   # 找到密码窗
    pyautogui.click()     # 点击
    
    pyautogui.typewrite('Fms1234567!',0.7)  # 输入密码

    pyautogui.moveTo(775,490, duration=0.5)   # 找到确定登录按钮
    pyautogui.click()     # 登录BSC客户端
    time.sleep(5)
    pyautogui.hotkey('altleft', 'y')
    
    pyautogui.moveTo(700,300, duration=20)   # 慢慢移动到屏幕中间等待网管加载
    
    # =============================================================================
    # 下发诊断测试取电压数据
    # =============================================================================
    pyautogui.hotkey('altleft', 'c')
    time.sleep(2)
    pyautogui.hotkey('altleft', 'o')
    time.sleep(2)
    pyautogui.hotkey('altleft', 'm')    # 通过热键打开中兴命令行工具
    time.sleep(3)

    pyautogui.moveTo(480,101, duration=20)   # 找到批处理标签
    pyautogui.click()     # 点击    
    pyautogui.moveTo(705,145, duration=0.5)   # 找到选择网元
    pyautogui.click()     # 点击    
    pyautogui.moveTo(506,217, duration=0.5)   # 选择OMMB1
    pyautogui.click()     # 点击    
    pyautogui.moveTo(680,405, duration=0.5)   # 找到确定
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(835,146, duration=0.5)   # 找到导入脚本按钮
    pyautogui.click()     # 点击    
    
    pyautogui.moveTo(626,513, duration=0.5)   # 找到文件名框
    pyautogui.click()     # 点击   
    
    pyautogui.typewrite('CMD1.txt',0.4)  # 输入文件名
    pyautogui.press('enter')
    pyautogui.hotkey('altleft', 'O') # 打开文件
    
    pyautogui.moveTo(731,145, duration=0.5)   # 找到运行按钮
    pyautogui.click()     # 点击    
    
    pyautogui.moveTo(685,495, duration=0.5)   # 找到确认执行按钮
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(700,300, duration=0.5)   # 移动到中间，等待任务结束
    time.sleep(160)   # 等待任务执行
    
    pyautogui.moveTo(835,146, duration=20)   # 找到导入脚本按钮
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(626,513, duration=0.5)   # 找到文件名输入框
    pyautogui.click()     # 点击   
    
    pyautogui.typewrite('CMD2.txt',0.4)  # 输入文件名
    pyautogui.press('enter')
    pyautogui.hotkey('altleft', 'O') # 打开文件   
    
    pyautogui.moveTo(731,145, duration=0.5)   # 找到运行按钮
    pyautogui.click()     # 点击    
    
    pyautogui.moveTo(685,495, duration=0.5)   # 找到确认执行按钮
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(700,300, duration=0.5)   # 移动到中间，等待任务结束
    time.sleep(160)   # 等待任务执行
    
    pyautogui.moveTo(835,146, duration=20)   # 找到导入脚本按钮
    pyautogui.click()     # 点击    
    
    pyautogui.moveTo(626,513, duration=0.5)   # 找到文件名输入框
    pyautogui.click()     # 点击    
    
    pyautogui.typewrite('CMD3.txt',0.4)  # 输入文件名
    pyautogui.press('enter')
    pyautogui.hotkey('altleft', 'O') # 打开文件    
    
    pyautogui.moveTo(731,145, duration=0.5)   # 找到运行按钮
    pyautogui.click()     # 点击    
    
    pyautogui.moveTo(685,495, duration=0.5)   # 找到确认执行按钮
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(700,300, duration=0.5)   # 移动到中间，等待任务结束
    time.sleep(160)   # 等待任务执行

            
    pyautogui.moveTo(705,145, duration=20)   # 找到选择网元
    pyautogui.click()     # 点击    
    pyautogui.moveTo(506,217, duration=0.5)   # 取消选择OMMB1
    pyautogui.click()     # 点击    
    pyautogui.moveTo(507,240, duration=0.5)   # 选择OMMB2
    pyautogui.click()     # 点击    
    pyautogui.moveTo(678,402, duration=0.5)   # 找到确定
    pyautogui.click()     # 点击    
    
    pyautogui.moveTo(835,146, duration=0.5)   # 找到导入脚本按钮
    pyautogui.click()     # 点击  
    
    pyautogui.moveTo(626,513, duration=0.5)   # 找到文件名框
    pyautogui.click()     # 点击
    
    pyautogui.typewrite('CMD4.txt',0.4)  # 输入文件
    pyautogui.press('enter')
    pyautogui.hotkey('altleft', 'O') # 打开文件

    pyautogui.moveTo(731,145, duration=0.5)   # 找到运行按钮
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(685,495, duration=0.5)   # 找到确认执行按钮
    pyautogui.click()     # 点击

    
    pyautogui.moveTo(700,300, duration=0.5)   # 移动到中间，画框，等待任务结束
    time.sleep(180)   # 等待任务执行
    
    pyautogui.moveTo(835,146, duration=20)   # 找到导入脚本按钮
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(626,513, duration=0.5)   # 找到文件名框
    pyautogui.click()     # 点击
    
    pyautogui.typewrite('CMD5.txt',0.4)  # 输入文件
    pyautogui.press('enter')
    pyautogui.hotkey('altleft', 'O') # 打开文件

    pyautogui.moveTo(731,145, duration=0.5)   # 找到运行按钮
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(685,495, duration=0.5)   # 找到确认执行按钮
    pyautogui.click()     # 点击

    
    pyautogui.moveTo(700,300, duration=0.5)   # 移动到中间，画框，等待任务结束
    time.sleep(200)   # 等待任务执行
    
    pyautogui.hotkey('altleft', 's') # 系统
    
    pyautogui.hotkey('altleft', 'u') # 注销
    time.sleep(3)     
    
    pyautogui.hotkey('altleft', 'y') # 确认注销
    time.sleep(6) 

    pyautogui.moveTo(895,320, duration=0.5)   # 关闭登陆窗
    pyautogui.click()
    pyautogui.moveTo(684,484, duration=0.5)   # 确认退出
    pyautogui.click()
        
    current_time = str(datetime.datetime.today()).split('.')[0]     # 获取当前时间信息
    print('任务结束时间:',current_time)   # 在cmd窗体中输出任务结束时间信息
    
    
    # =============================================================================
    # 采集转储原始文件    
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
        shutil.copy(data_path + copyfile, bak_path)     #将文件备份到 bakpath 
    current_time =str(datetime.now()).split('.')[0]
    print(current_time + ' '+ '数据入库完成：本次入库 %d 个文件!' % len(file_list))
    
    for deletefile in file_list: 
        os.remove(data_path + deletefile)   # 备份完成后，删除源文件
    
    # =============================================================================
    # 处理电压数据                  
    # =============================================================================    
    def get_data_info(file):    # 定义从文件中获取日期信息的函数
        data_array = file.split('-')[3]
        time_array1 = file.split('-')[4]
        time_array2 = file.split('-')[5]
        time_info =  data_array[0:4] + '-' + data_array[4:6] + '-' + data_array[6:] + ' ' + time_array1[0:2]+ ':' + time_array1[2:] + ':' + time_array2[0:2]
        return time_info

    calc_file = []
    bak_files = os.listdir(bak_path) 
    for file in bak_files :
        if (get_data_info(file).split(' ')[0] == today or 
            get_data_info(file).split(' ')[0] == yestoday):
            calc_file.append(file)
    
    df_eNodeB_name = pd.read_excel(out_path + eNodeB_name ,dtype =str,encoding='utf-8') 
    df_eNodeB_name['eNodeB'] =df_eNodeB_name['eNodeB'].astype(int)  # 打开eNodeB_name表格，并处理数据格式

    df_vol=pd.DataFrame(columns=['基站名称','区县','eNodeB','直流电压','采集时间'])     # 用于装电压原始数据
    df_power_down = pd.DataFrame(columns=['基站名称','区县','eNodeB','当前电压',
            '市电状态','停电时间','持续时间','恢复时间','数据更新时间'])  # 停电基站表，用于装停电基站
    
    if len(calc_file) > 0:
        for vofile_name in calc_file:        
            collect_time = get_data_info(vofile_name)  # 通过文件名提取时间信息
            file_tmp1 = open(bak_path + vofile_name,'r',encoding='gbk')  # 用零时文件读取原始记录文件
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
                if df_btsvol.loc[k,'市电状态'] =='' and df_btsvol.loc[k+1,'市电状态'] =='停电' and df_btsvol.loc[k+1,'直流电压'] < 55 :
                    break_time.append(df_btsvol.loc[k+1,'采集时间'])
                elif df_btsvol.loc[k,'市电状态'] =='来电' and df_btsvol.loc[k+1,'市电状态'] =='停电' and df_btsvol.loc[k+1,'直流电压'] < 55 :
                    break_time.append(df_btsvol.loc[k+1,'采集时间'])
                elif df_btsvol.loc[k,'市电状态'] =='' and df_btsvol.loc[k+1,'市电状态'] =='来电' and df_btsvol.loc[k+1,'直流电压'] <54:
                    resume_time.append(df_btsvol.loc[k+1,'采集时间'])
                elif df_btsvol.loc[k,'市电状态'] =='停电' and df_btsvol.loc[k+1,'市电状态'] =='来电' and df_btsvol.loc[k+1,'直流电压'] <54:
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
                #对第一次停电时间去重
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
        
        current_time = str(datetime.today()).split('.')[0]
        print('报表完成时间:',current_time)
        print('---------------------------------')
        current_time = current_time.replace(':','.')
        
        with pd.ExcelWriter(out_path + current_time + '_实时停电报表.xlsx') as writer:
            df_power_down.to_excel(writer,current_time +'_停电记录') 

# =============================================================================
# 定义电压日报任务的函数
# =============================================================================
def report_task():
    
    sche.enter(86400,1,report_task)  # 调用sche实力的enter方法创建一个定时任务，86400秒之后执行，任务内容执行report_task()函数
    current_time = str(datetime.now()).split('.')[0]
    print('日报开始时间:',current_time)   # 在cmd窗体中输出任务开始时间信息
    
    def get_data_info(vofile):
        data_array = vofile.split('-')[3]
        time_array = vofile.split('-')[4] + vofile.split('-')[5][0:2]
        time_info = data_array[0:4] + '-' + data_array[4:6] + '-' + data_array[6:] + ' ' + time_array[0:2] + ':' + time_array[2:4] + ':' + time_array[4:]
        return time_info
    
    today = datetime.today()
    yestoday = today - timedelta(days=1)
    yestoday = str(yestoday).split(' ')[0]
    
    all_files = os.listdir(bak_path)
    file_ommb1=[]
    file_ommb2=[]
    for vofile in all_files:
        if 'QJ_OMMB1' in vofile:
            if  get_data_info(vofile).split(' ')[0] == yestoday :
                file_ommb1.append(vofile)  # 找出昨天天采集的所有文件
        elif 'QJ_OMMB2' in vofile:
            if  get_data_info(vofile).split(' ')[0] == yestoday :
                file_ommb2.append(vofile)  # 找出昨天天采集的所有文件
    
    
    df_OMMB1 = pd.read_excel(out_path + OMMB1 ,encoding='utf-8') 
    df_OMMB2 = pd.read_excel(out_path + OMMB2 ,encoding='utf-8') 
        
    df_ommb1_name = df_OMMB1[['eNodeB']]    # 注意这里一定是双括号，如果是单括号，
    df_ommb2_name = df_OMMB2[['eNodeB']]    # 取到的只是一列，而不是一个表，就不能进行merge等操作
    df_result = pd.DataFrame()
    
    def collect_voinfo(file):
        collect_time = get_data_info(file)  # 通过文件名提取时间信息
        with open(bak_path + file,'r',encoding='gbk') as file_tmp:
            content = file_tmp.readlines() 
            df_tmp = pd.DataFrame(columns=['eNodeB','直流电压','采集时间'])
            for i in range(0,len(content)-5,1):            
                if 'NE=' in  content[i] and 'PM单板诊断测试' in  content[i+5]:
                    df_tmp.loc[i,'eNodeB']= content[i].split(',')[1][3:]
                    df_tmp.loc[i,'采集时间']= collect_time
                    df_tmp.loc[i,'直流电压']= float(content[i+5].split('    ')[3].split(' ')[4][:-1])
        return df_tmp
        
    if len(file_ommb1) > 0:
        n=0     # 编号n表示同一时间段的第几次采集
        df_tmp = pd.DataFrame(columns=['eNodeB','直流电压','采集时间'])   # 零时表格用来汇总每次采集的几个数据
        for i in range(0,len(file_ommb1)-2,1):        
            df_tmp = df_tmp.append(collect_voinfo(file_ommb1[i]),ignore_index=True)
            # 计算两个采集文件的时间差
            time_interval = (datetime.strptime(get_data_info(file_ommb1[i+1]),"%Y-%m-%d %H:%M:%S") 
                            - datetime.strptime(get_data_info(file_ommb1[i]),"%Y-%m-%d %H:%M:%S")).seconds 
            if time_interval < 360: # 如果采集时间差小于360秒，则是同一次采集，把数据追加在一起
                df_tmp = df_tmp.append(collect_voinfo(file_ommb1[i+1]),ignore_index=True)
            elif time_interval > 360: # 如果采集时间差大于360秒，本次采集结束，则将数据汇总到最终结果df_OMMB1中
                n += 1
                df_tmp = df_tmp.groupby(by='eNodeB',as_index=False)[['直流电压','采集时间']].max()
                df_tmp['eNodeB'] = df_tmp['eNodeB'].astype(int) 
                df_tmp = pd.merge(df_ommb1_name,df_tmp,how='left',on = 'eNodeB')              
                df_OMMB1['时间_%s' %str(n)] = df_tmp['采集时间']
                df_OMMB1['电压_%s' %str(n)] = df_tmp['直流电压']
                df_tmp = pd.DataFrame(columns=['eNodeB','直流电压','采集时间'])
    
    if len(file_ommb2) > 0:
        n = 0
        df_tmp = pd.DataFrame(columns=['eNodeB','直流电压','采集时间'])
        for i in range(0,len(file_ommb2)-1,1):
            df_tmp = df_tmp.append(collect_voinfo(file_ommb2[i]),ignore_index=True)
            # 计算两个采集文件的时间差
            time_interval = (datetime.strptime(get_data_info(file_ommb2[i+1]),"%Y-%m-%d %H:%M:%S") 
                            - datetime.strptime(get_data_info(file_ommb2[i]),"%Y-%m-%d %H:%M:%S")).seconds 
            if time_interval < 360: # 如果采集时间差小于360秒，则是同一次采集，把数据追加在一起
                df_tmp = df_tmp.append(collect_voinfo(file_ommb2[i+1]),ignore_index=True)
            elif time_interval > 360: # 如果采集时间差大于360秒，本次采集结束，则数据汇总到最终结果中
                n += 1
                df_tmp = df_tmp.groupby(by='eNodeB',as_index=False)[['直流电压','采集时间']].max()
                df_tmp['eNodeB'] = df_tmp['eNodeB'].astype(int) 
                df_tmp = pd.merge(df_ommb2_name,df_tmp,how='left',on = 'eNodeB')              
                df_OMMB2['时间_%s' %str(n)] = df_tmp['采集时间']
                df_OMMB2['电压_%s' %str(n)] = df_tmp['直流电压']
                df_tmp = pd.DataFrame(columns=['eNodeB','直流电压','采集时间'])
                
    df_result = df_result.append(df_OMMB1,ignore_index=True)
    df_result = df_result.append(df_OMMB2,ignore_index=True)  
    df_result = df_result.fillna('-')
    cols = ['eNodeB','网元名称']
    for i in range(1,int(len(df_result.columns)/2),1):
        cols.append('时间_' + str(i))
        cols.append('电压_' + str(i))
    df_result = df_result[cols]
          
    current_time = str(datetime.now()).split(' ')[0]
    with pd.ExcelWriter(out_path + current_time + '_LTE基站电压日报.xlsx')  as  writer :
        df_result.to_excel(writer,current_time +'_电压日报') 
        
    print('日报完成时间:',current_time)   # 在cmd窗体中输出日报任务完成时间信息


    
sche.enter(12,1,collect_task)  # 调用sche实力的enter方法创建一个定时任务，12秒之后执行，任务内容执行 collect_task()函数
sche.enter(15,1,report_task)  # 调用sche实力的enter方法创建一个定时任务，15秒之后执行，任务内容执行 report_task()函数

print('task will run in 10 second') # 提示信息 10秒计时
for i in range(1,11,1):
    print('----->',i)
    time.sleep(1)

sche.run()
   
    
    
    
    
    
    
    
