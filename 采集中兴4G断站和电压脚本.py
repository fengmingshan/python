# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 10:41:21 2018

@author: Administrator
"""
import pyautogui # 
import sched # 导入定时任务库
import time # 导入time模块
import os
import pandas as pd


sche=sched.scheduler(time.time,time.sleep)  # 实例化sched.scheduler类

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1.5  # 停顿2秒
pyautogui.size()
width, height = pyautogui.size()

def get_current_time():     # 定义获取当前时间的函数
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

def task():
    sche.enter(1800,1,task)  # 调用sche实力的enter方法创建一个定时任务，1800秒之后执行，任务内容执行task()函数
    current_time = get_current_time()
    print('任务开始时间:',current_time)

# =============================================================================
# 登陆BSC    
# =============================================================================
    pyautogui.moveTo(109,246, duration=0.5)   # 找到BSC客户端
    pyautogui.doubleClick()     # 双击打开BSC客户端
    
    pyautogui.moveTo(649,480, duration=0.5)   # 找到密码窗
    pyautogui.click()     # 点击
    
    pyautogui.typewrite('Fms1234567!',0.5)  # 输入密码
    
    
    pyautogui.moveTo(809,557, duration=0.5)   # 找到登录按钮
    pyautogui.click()     # 登录BSC客户端
    
    time.sleep(15)
    
# =============================================================================
# 取传输状态
# =============================================================================
    
    pyautogui.hotkey('altleft', 'c')

    pyautogui.hotkey('altleft', 'o')
    
    pyautogui.hotkey('altleft', 'm')
    time.sleep(5)
    
    pyautogui.moveTo(561,100, duration=0.5)   # 找到批处理标签
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(785,145, duration=0.5)   # 找到选择网元
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(586,217, duration=0.5)   # 选择OMMB1
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(753,404, duration=0.5)   # 找到确定
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(913,148, duration=0.5)   # 找到导入脚本按钮
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(640,511, duration=0.5)   # 找到文件名框
    pyautogui.click()     # 点击
    
    pyautogui.typewrite('SCTP_ommb1.txt',0.4)  # 输入文件名
    pyautogui.press('enter')
    
    pyautogui.moveTo(808,144, duration=0.5)   # 找到运行按钮
    pyautogui.click()     # 点击
    time.sleep(240)
        
    pyautogui.moveTo(504,433, duration=0.5)   # 找到另存文件按钮
    pyautogui.click()     # 点击
    
    time_now1 = get_current_time()
    time_now1 = time_now1.replace(':','.')
    pyautogui.typewrite(time_now1,0.4)  # 输入时间信息
    
    pyautogui.moveTo(829,574, duration=0.5)   # 找到保存文件按钮
    pyautogui.click()     # 点击    
    time.sleep(2)   # 等待保存
    
    pyautogui.moveTo(717,486, duration=0.5)   # 找到确定
    pyautogui.click() # 点击    
    
    pyautogui.moveTo(785,145, duration=0.5)   # 找到选择网元
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(586,217, duration=0.5)   # 取消选择OMMB1
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(585,240, duration=0.5)   # 选择OMMB2
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(753,404, duration=0.5)   # 找到确定
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(913,148, duration=0.5)   # 找到导入脚本按钮
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(640,511, duration=0.5)   # 找到文件名框
    pyautogui.click()     # 点击
    
    pyautogui.typewrite('SCTP_ommb2.txt',0.4)  # 输入文件
    pyautogui.press('enter')
    
    pyautogui.moveTo(808,144, duration=0.5)   # 找到运行按钮
    pyautogui.click()     # 点击
    time.sleep(210)
    
    pyautogui.moveTo(504,433, duration=0.5)   # 找到另存文件按钮
    pyautogui.click()     # 点击
    
    time_now2 = get_current_time()
    time_now2 = time_now2.replace(':','.')
    pyautogui.typewrite(time_now2,0.4)  # 输入时间信息
      
    pyautogui.moveTo(829,574, duration=0.5)   # 找到保存文件按钮
    pyautogui.click()    # 点击
    time.sleep(2) #等待保存
    
    pyautogui.moveTo(717,486, duration=0.5)   # 找到确定
    pyautogui.click() # 点击    


# =============================================================================
#   取电压数据  
# =============================================================================
    pyautogui.hotkey('altleft', 'c')
    
    pyautogui.hotkey('altleft', 'e')
    # =============================================================================
    # OMMB1
    # =============================================================================
    pyautogui.moveTo(160,152, duration=0.5)   # 找OMMB1
    pyautogui.click(button='right') 
    pyautogui.moveRel(63,13, duration=0.5)   # 启动网元管理
    pyautogui.click() 
    time.sleep(40)
    
    pyautogui.moveTo(160,152, duration=0.5)   # 找OMMB1
    pyautogui.click(button='right') 
    pyautogui.moveRel(46,129, duration=0.5)   # 找诊断测试
    pyautogui.click() 
    time.sleep(15)
    
    
    
    pyautogui.hotkey('altleft', 'o')
    
    pyautogui.hotkey('altleft', 't')
    
    pyautogui.moveTo(661,242, duration=0.5)   # 找到任务直流输入电压
    pyautogui.click(button='right') 
    pyautogui.moveRel(34,129, duration=0.5)   # 找到运行
    pyautogui.click() 
    pyautogui.moveTo(689,485, duration=0.5)   # 确定开始运行
    pyautogui.click() 
    
    
    pyautogui.moveTo(700,300, duration=0.5)   # 移动到中间，画框，等待任务结束
    for i in range(0,10,1):                   # 画10次，时间55秒左右
        pyautogui.moveTo(850,300, duration=0.5)   # 画框
        pyautogui.moveTo(850,450, duration=0.5)   # 画框
        pyautogui.moveTo(700,450, duration=0.5)   # 画框
        pyautogui.moveTo(700,300, duration=0.5)   # 画框
        time.sleep(1)   # 等待任务执行
    
    
    pyautogui.moveTo(661,241, duration=0.5)   # 找到任务找到任务直流输入电压
    pyautogui.click(button='right') 
    pyautogui.moveRel(44,152, duration=0.5)   # 选择查看任务结果
    pyautogui.click() 
    pyautogui.moveTo(972,178, duration=0.5)   # 找到导出任务结果
    pyautogui.click() 
    pyautogui.moveTo(860,574, duration=0.5)   # 找到保存
    pyautogui.click() 
    time.sleep(15)
    pyautogui.moveTo(680,485, duration=2)   # 不转到目录
    pyautogui.click()
    pyautogui.moveTo(682,150, duration=1)   # 关闭查询结果
    pyautogui.click()
    
    time.sleep(5)
    
    # =============================================================================
    # OMMB2
    # =============================================================================
    pyautogui.moveTo(155,178, duration=0.5)   # 找OMMB2
    pyautogui.click(button='right') 
    pyautogui.moveRel(63,13, duration=0.5)   # 启动网元管理
    pyautogui.click() 
    time.sleep(40)
    
    pyautogui.moveTo(155,178, duration=0.5)   # 找OMMB2
    pyautogui.click(button='right') 
    pyautogui.moveRel(46,129, duration=0.5)   # 找诊断测试
    pyautogui.click() 
    time.sleep(15)
    
    
    
    pyautogui.hotkey('altleft', 'o')
    
    pyautogui.hotkey('altleft', 't')
        
    pyautogui.moveTo(661,242, duration=0.5)   # 找到任务直流输入电压
    pyautogui.click(button='right') 
    pyautogui.moveRel(34,129, duration=0.5)   # 找到运行
    pyautogui.click() 
    pyautogui.moveTo(689,485, duration=0.5)   # 确定开始运行
    pyautogui.click() 
    
    
    pyautogui.moveTo(700,300, duration=0.5)   # 移动到中间，画框，等待任务结束
    for i in range(0,8,1):                   # 画6次，时间30秒左右
        pyautogui.moveTo(850,300, duration=0.5)   # 画框
        pyautogui.moveTo(850,450, duration=0.5)   # 画框
        pyautogui.moveTo(700,450, duration=0.5)   # 画框
        pyautogui.moveTo(700,300, duration=0.5)   # 画框
        time.sleep(1)   # 等待任务执行
        
    pyautogui.moveTo(661,241, duration=0.5)   # 找到任务找到任务直流输入电压
    pyautogui.click(button='right') 
    pyautogui.moveRel(44,152, duration=0.5)   # 选择查看任务结果
    pyautogui.click() 
    pyautogui.moveTo(972,178, duration=0.5)   # 找到导出任务结果
    pyautogui.click() 
    pyautogui.moveTo(860,574, duration=0.5)   # 找到保存
    pyautogui.click() 
    time.sleep(15)
    pyautogui.moveTo(680,485, duration=0.5)   # 不转到目录
    pyautogui.click()
    pyautogui.moveTo(682,150, duration=0.5)   # 关闭查询结果
    pyautogui.click()
    time.sleep(5)
    
    pyautogui.hotkey('altleft', 's') # 系统
    
    pyautogui.hotkey('altleft', 'u') # 注销
    
    pyautogui.moveTo(680,487, duration=0.5)   # 确认注销
    pyautogui.click()
    time.sleep(10) 
    pyautogui.moveTo(891,320, duration=0.5)   # 关闭登陆窗
    pyautogui.click()
    pyautogui.moveTo(684,484, duration=0.5)   # 确认退出
    pyautogui.click()
    
    current_time = get_current_time()
    print('任务结束时间:',current_time)
    
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
    data_path = r'C:\Users\lenovo'+'\\'
    out_path = r'F:\_中兴4G网管断站与停电'+'\\'
    eNodeB_name='eNode_name.xls'
    df_eNodeB_name = pd.read_excel(data_path +eNodeB_name ,dtype =str,encoding='utf-8') 
    
    all_files = os.listdir(data_path) 
    file_list=[]
    for file in all_files:
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
# =============================================================================
# 处理电压数据                  
# =============================================================================
    voltage_path =r'E:\netnumen\ems\ums-client\rundata\dtm'+'\\'
    vo_files = os.listdir(voltage_path)
    
    vo_file_list=[]
    for vofile in vo_files:
        if 'export-' in vofile:
            if str(int(vofile[11:13]))+'月'+str(int(vofile[13:15]))+'日' == month_day:
                vo_file_list.append(vofile)  # 找出今天采集的所有文件
    
    df_vol=pd.DataFrame(columns=['网元名称','区县','基站代码','直流电压','采集时间'])     # 用户装原始数据
    df_power_down = pd.DataFrame(columns=['网元名称','区县','基站代码','当前电压',
            '市电状态','停电时间','恢复时间','数据更新时间'])  # 停电基站表，用于装停电基站
    
    if len(vo_file_list) > 0:
        for vofile_name in vo_file_list:
            time_str = vofile_name[7:15]+vofile_name[16:22] # 取出采集时间字符串
            time_array=(int(time_str[0:4]),int(time_str[4:6]),int(time_str[6:8]),int(time_str[8:10]),int(time_str[10:12]),int(time_str[12:14]),5,50,1) # 转换采集时间为struct_time
            collect_time=time.strftime('%Y/%m/%d %H:%M:%S',time_array) # 转换采集时间为正常时间格式
            
            df_tmp = pd.read_csv(voltage_path + vofile_name,encoding='GBK') 
            df_tmp=df_tmp[df_tmp['测试项'].str.contains('输入电源电压')]
            
            df_tmp['网元名称']=df_tmp['网元名称'].map(lambda x:x.replace('整治-',''))
            df_tmp['网元名称']=df_tmp['网元名称'].map(lambda x:x.replace('整治_',''))
            df_tmp['网元名称']=df_tmp['网元名称'].map(lambda x:x.replace('调测-',''))
            df_tmp['网元名称']=df_tmp['网元名称'].map(lambda x:x.replace('调测_',''))
                
            df_voltage=pd.DataFrame(columns=['网元名称','区县','基站代码','直流电压','采集时间'])
            
            df_voltage['网元名称']=df_tmp['网元名称']
            df_voltage['区县']=df_tmp['网元名称'].map(lambda x:x.split('_')[1][2:4])
            df_voltage['基站代码']= df_tmp['网元'].map(lambda x:x.split('=')[2])
            df_voltage['采集时间']= collect_time
            df_voltage['直流电压']= df_tmp['测试结果'].map(lambda x:x[:-1])
            df_voltage['直流电压']= df_voltage['直流电压'].astype(float)
            df_vol=df_vol.append(df_voltage,ignore_index=True)
            df_vol=df_vol.reset_index()
            del df_vol['index']
        
        df_low_power = df_vol[df_vol['直流电压']<50]     # 筛选电池电压低于50v的基站，可能发生了停电
        if len(df_low_power)>0:
            low_power_bts =  list(set(list(df_low_power['基站代码']))) #通过转换为set去重复
            for i in range(0,len(low_power_bts),1):
                df_down_tmp = pd.DataFrame(columns=['网元名称','区县','基站代码','当前电压',
                    '市电状态','停电时间','恢复时间','数据更新时间'])
                df_btsvol = df_vol[df_vol['基站代码']== low_power_bts[i]]
                df_btsvol = df_btsvol.reset_index()
                break_bts = []  # 用来存储停电基站列表
                break_country = []  # 用来存储区县
                bts_id = []   # 用来存储基站代码
                now_voltage=[] # 用来存储当前电压
                power_state=[]  # 用来存储市电状态
                start_time = []  # 用来存储停电时间
                end_time = []    # 用来存储恢复时间
                updata_time=[]  # 用来存储数据更新时间
                for j in range(0,len(df_btsvol)-1,1):
                    df_btsvol.loc[j,'电压差']=df_btsvol.loc[j,'直流电压']-df_btsvol.loc[j+1,'直流电压']
                    if df_btsvol.loc[j,'电压差'] > 1:
                        break_bts.append(df_btsvol.loc[0,'网元名称'])
                        break_country.append(df_btsvol.loc[0,'区县'])
                        bts_id.append(df_btsvol.loc[0,'基站代码'])
                        now_voltage.append(df_btsvol.loc[len(df_btsvol)-1,'直流电压'])
                        power_state.append('停电')
                        start_time.append( df_btsvol.loc[j+1,'采集时间'])
                        updata_time.append(df_btsvol.loc[len(df_btsvol)-1,'采集时间'])
                    elif df_btsvol.loc[j,'电压差'] < -2:
                        end_time.append(df_btsvol.loc[j+1,'采集时间'])
                    if len(end_time)>0 and len(start_time)>0:
                        if time.strptime(start_time[0],'%Y/%m/%d %H:%M:%S') > time.strptime(end_time[0],'%Y/%m/%d %H:%M:%S'):
                            del end_time[0]
                    for k in range(0,len(break_bts),1):
                        df_down_tmp.loc[k,'网元名称'] = break_bts[k]
                        df_down_tmp.loc[k,'区县'] = break_country[k]
                        df_down_tmp.loc[k,'基站代码'] = bts_id[k]
                        df_down_tmp.loc[k,'当前电压'] = now_voltage[k]
                        df_down_tmp.loc[k,'市电状态'] = power_state[k]
                        df_down_tmp.loc[k,'停电时间'] = start_time[k]
                        df_down_tmp.loc[k,'数据更新时间'] = updata_time[k]
                    for k in range(0,len(end_time),1):
                            df_down_tmp.loc[k,'恢复时间'] = end_time[k]
                df_power_down = df_power_down.append(df_down_tmp,ignore_index=True)
# =============================================================================
#  输出结果                   
# =============================================================================
    writer = pd.ExcelWriter(out_path + month_day + sheet_time + '基站断站及停电.xls')
    df_result.to_excel(writer,sheet_time + '_断站') 
    df_power_down.to_excel(writer,sheet_time + '_停电') 
    writer.save()
    
    current_time = get_current_time()
    print('报表完成时间:',current_time)
    print('-----------------------------------')




sche.enter(12,1,task)  # 调用sche实力的enter方法创建一个定时任务，12秒之后执行，任务内容执行task()函数

print('task will run in 10 second') # 提示信息 10秒计时
for i in range(1,11,1):
    print('----->',i)
    time.sleep(1)

sche.run()
   
    
    
    
    
    
    
    
