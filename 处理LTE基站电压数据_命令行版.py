# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 09:58:45 2018

@author: Administrator
"""
import os
import pandas as pd 
import datetime

# =============================================================================
# 设置环境变量
# =============================================================================
voltage_path = r'D:\4G_voltage'+'\\'
out_path = r'D:\4G_voltage'+'\\'
eNodeB_name = 'eNode_name.xls'
#==============================================================================
# 定义获取当前时间信息的函数
#==============================================================================
def get_vofile_time(vofile):
    data_array = vofile.split('-')[2]
    time_array = vofile.split('-')[3] + vofile.split('-')[4][0:2]
    time_info = data_array[0:4] + '-' + data_array[4:6] + '-' + data_array[6:] + ' ' + time_array[0:2] + ':' + time_array[2:4] + ':' + time_array[4:]
    return time_info

today = datetime.datetime.today()
yestoday = today - datetime.timedelta(days=1)
today = str(today).split(' ')[0]
yestoday = str(yestoday).split(' ')[0]

vo_files = os.listdir(voltage_path)
vo_file_list=[]
for vofile in vo_files:
    if '-BatchResult-' in vofile:
        if get_vofile_time(vofile).split(' ')[0] == today or\
        get_vofile_time(vofile).split(' ')[0] == yestoday :
            vo_file_list.append(vofile)  # 找出今天采集的所有文件

df_eNodeB_name = pd.read_excel(voltage_path +eNodeB_name ,encoding='utf-8') 
df_vol=pd.DataFrame(columns=['网元名称','区县','基站代码','直流电压','采集时间'])     # 用于装电压原始数据
df_power_down = pd.DataFrame(columns=['网元名称','区县','基站代码','当前电压',
        '市电状态','停电时间','持续时间','恢复时间','数据更新时间'])  # 停电基站表，用于装停电基站

if len(vo_file_list) > 0:
    for vofile_name in vo_file_list:        
        collect_time = get_vofile_time(vofile_name)  # 通过文件名提取时间信息
        file_tmp = open(voltage_path + vofile_name,'r',encoding='gbk')  # 用零时文件读取原始记录文件
        content = file_tmp.readlines() 
        df_tmp=pd.DataFrame(columns=['网元名称','区县','基站代码','直流电压','采集时间'])
        for i in range(0,len(content),1):
            if 'NE=' in  content[i] and 'PM单板诊断测试' in  content[i+5]:
                df_tmp.loc[i,'基站代码']= content[i].split(',')[1][3:]
                df_tmp.loc[i,'采集时间']= collect_time
                df_tmp.loc[i,'直流电压']= float(content[i+5].split('    ')[3].split(' ')[4][:-1])
        df_vol=df_vol.append(df_tmp,ignore_index=True)  
        df_vol['基站代码'] = df_vol['基站代码'].astype(int)
        df_vol = pd.merge(df_vol,df_eNodeB_name,how = 'left',on = '基站代码')
        df_vol['网元名称'] = df_vol['基站名称']
        df_vol['区县']=df_vol['网元名称'].map(lambda x:x.split('_')[1][2:4])
        df_vol = df_vol.groupby(by='网元名称',as_index=False)[['区县','基站代码','直流电压','采集时间']].max()
        df_vol=df_vol.reset_index()
        del df_vol['index']
    
    df_low_power = df_vol[df_vol['直流电压']<50]     # 筛选电池电压低于50v的基站，可能发生了停电
    low_power_bts =  list(set(list(df_low_power['基站代码']))) #通过转换为set去重复
    for i in range(0,len(low_power_bts)-1,1):        
        df_btsvol = df_vol[df_vol['基站代码']== low_power_bts[i]]
        df_btsvol = df_btsvol.reset_index()
        df_btsvol['市电状态'] = ''
        if len(df_btsvol)>=2:
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
    
    current_time = str(datetime.datetime.today())
    current_time = current_time.split('.')[0].replace(':','.')
    writer = pd.ExcelWriter(out_path + current_time + '基站断站及停电.xls')
    df_power_down.to_excel(writer,'停电') 
    df_vol.to_excel(writer,'原始记录') 
    writer.save()
    

    




