# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 09:58:45 2018

@author: Administrator
"""
import os
import pandas as pd 
import time

#==============================================================================
# 定义获取当前时间信息的函数
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

voltage_path =r'D:\4G_voltage'+'\\'
vo_files = os.listdir(voltage_path)

def get_vofile_time(vofile):
    data_array = vofile.split('-')[1][0:8]
    time_array = vofile.split('_')[1][0:6]
    time_info = data_array[0:4] + '-' + data_array[4:6] + '-' + data_array[6:] + ' ' + time_array[0:2] + ':' + time_array[2:4] + ':' + time_array[4:]
    return time_info

current_time = get_current_time()
#today = current_time.split(' ')[0]
today = '2018-03-21'

vo_file_list=[]
for vofile in vo_files:
    if 'export-' in vofile:
        if get_vofile_time(vofile).split(' ')[0] == today:
            vo_file_list.append(vofile)  # 找出今天采集的所有文件

df_vol=pd.DataFrame(columns=['网元名称','区县','基站代码','直流电压','采集时间'])     # 用于装电压原始数据
df_power_down = pd.DataFrame(columns=['网元名称','区县','基站代码','当前电压',
        '市电状态','停电时间','持续时间','恢复时间','数据更新时间'])  # 停电基站表，用于装停电基站

if len(vo_file_list) > 0:
    for vofile_name in vo_file_list:
        
        collect_time = get_vofile_time(vofile_name)  # 通过文件名提取时间信息
        
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
        df_voltage = df_voltage.groupby(by='网元名称',as_index=False)[['区县','基站代码','直流电压','采集时间']].max()
        df_vol=df_vol.append(df_voltage,ignore_index=True)
        df_vol=df_vol.reset_index()
        del df_vol['index']
    
    df_low_power = df_vol[df_vol['直流电压']<50]     # 筛选电池电压低于50v的基站，可能发生了停电
    low_power_bts =  list(set(list(df_low_power['基站代码']))) #通过转换为set去重复
    for i in range(0,len(low_power_bts)-1,1):        
        df_btsvol = df_vol[df_vol['基站代码']== low_power_bts[i]]
        df_btsvol = df_btsvol.reset_index()
        df_btsvol['市电状态'] = ''
        if df_btsvol.loc[len(df_btsvol)-1,'直流电压'] -df_btsvol.loc[len(df_btsvol)-2,'直流电压'] <= -0.3:   #计算电压差，最后一行需要单独计算
            df_btsvol.loc[len(df_btsvol)-1,'市电状态'] = '停电'
        elif df_btsvol.loc[len(df_btsvol)-1,'直流电压'] -df_btsvol.loc[len(df_btsvol)-2,'直流电压'] >= 0.3: 
            df_btsvol.loc[len(df_btsvol)-1,'市电状态'] = '来电'

        for j in range(1,len(df_btsvol)-1,1):
            if df_btsvol.loc[j,'直流电压'] - df_btsvol.loc[j+1,'直流电压'] >= 0.3:      # 循环计算电压差，得到市电状态
                df_btsvol.loc[j+1,'市电状态'] = '停电'
            elif df_btsvol.loc[j,'直流电压'] - df_btsvol.loc[j+1,'直流电压'] <= -0.3:
                df_btsvol.loc[j,'市电状态'] = '来电'
    
        df_down_tmp = pd.DataFrame(columns=['网元名称','区县','基站代码','当前电压',
            '市电状态','停电时间','持续时间','恢复时间','数据更新时间'])
        start_time = df_btsvol.loc[0,'采集时间']  
        end_time = df_btsvol.loc[len(df_btsvol)-1,'采集时间']     
        break_time = [] # 用来存储停电时间
        resume_time = [] # 用来存储恢复时间
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
            break_time.insert(0,start_time)     # 如果break_time没有值，则说明停电发生在更早的时间，则视为发生在start_time
        elif len(break_time) > 0 and  len(resume_time) > 0:
            if time.strptime(resume_time[0],'%Y-%m-%d %H:%M:%S') < time.strptime(break_time[0],'%Y-%m-%d %H:%M:%S') : 
                break_time.insert(0,start_time)     # 如果第一次回复时间比第一次停电时间还早，则说明在start_time之前发生了停电
            break_time_copy = break_time[:]    # [:]是深拷贝，注意这里还有有个大坑，详见下面的注释。 
            if len(break_time) > len(resume_time):
                for element in break_time_copy:
                    if  break_time_copy.index(element) > len(resume_time)-1 and time.strptime(element,'%Y-%m-%d %H:%M:%S') < time.strptime(resume_time[len(resume_time)-1],'%Y-%m-%d %H:%M:%S'):
                        break_time.remove(element)
# =============================================================================
#   注意这里有个大坑，如果通过循环遍历删除list：break_time中的元素，list后面的元素会自动向上补位，导致循环报错
#   所有需要复制一份list的副本作为循环的条件，然后删除原list中的值                      
# =============================================================================
        for n in range(0,len(break_time),1):
            df_down_tmp.loc[n,'网元名称'] = df_btsvol.loc[0,'网元名称']
            df_down_tmp.loc[n,'区县'] = df_btsvol.loc[0,'区县']
            df_down_tmp.loc[n,'基站代码'] = df_btsvol.loc[0,'基站代码']
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
    
    current_time = get_current_time()
    current_time = current_time.replace(':','.')
    writer = pd.ExcelWriter(voltage_path + current_time + '基站断站及停电.xls')
    df_power_down.to_excel(writer,'停电') 
    df_vol.to_excel(writer,'原始记录') 
    writer.save()
    

    




