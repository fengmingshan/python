# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 09:58:45 2018

@author: Administrator
"""
import os
import pandas as pd 
from datetime import datetime
import time

# =============================================================================
# 设置环境变量
# =============================================================================
data_path = r'D:\4G_voltage'+'\\'
out_path = r'D:\4G_voltage'+'\\'
eNodeB_name = 'eNode_name.xls'
#==============================================================================
# 定义获取当前时间信息的函数
#==============================================================================
def get_data_info(vofile):
    data_array = vofile.split('-')[3]
    time_array = vofile.split('-')[4] + vofile.split('-')[5][0:2]
    time_info = data_array[0:4] + '-' + data_array[4:6] + '-' + data_array[6:] + ' ' + time_array[0:2] + ':' + time_array[2:4] + ':' + time_array[4:]
    return time_info

today = datetime.datetime.today()
yestoday = today - datetime.timedelta(days=1)
today = str(today).split(' ')[0]
yestoday = str(yestoday).split(' ')[0]

vo_files = os.listdir(data_path)
file_list=[]
for vofile in vo_files:
    if 'QJ_OMMB' in vofile:
        if get_data_info(vofile).split(' ')[0] == today or\
        get_data_info(vofile).split(' ')[0] == yestoday :
            file_list.append(vofile)  # 找出今天采集的所有文件

df_eNodeB_name = pd.read_excel(data_path +eNodeB_name ,encoding='utf-8') 
df_vol=pd.DataFrame(columns=['基站名称','区县','eNodeB','直流电压','采集时间'])     # 用于装电压原始数据
df_power_down = pd.DataFrame(columns=['基站名称','区县','eNodeB','当前电压',
        '市电状态','停电时间','持续时间','恢复时间','数据更新时间'])  # 停电基站表，用于装停电基站

if len(file_list) > 0:
    for vofile_name in file_list:        
        collect_time = get_data_info(vofile_name)  # 通过文件名提取时间信息
        file_tmp1 = open(data_path + vofile_name,'r',encoding='gbk')  # 用零时文件读取原始记录文件
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
        df_btsvol = df_vol[df_vol['eNodeB']== low_power_bts[i]]
        df_btsvol = df_btsvol.reset_index()
        df_btsvol['市电状态'] = ''
        if len(df_btsvol) >= 2 :
            if df_btsvol.loc[len(df_btsvol)-1,'直流电压'] -df_btsvol.loc[len(df_btsvol)-2,'直流电压'] <= -0.3:   #计算电压差，最后一行需要单独计算
                df_btsvol.loc[len(df_btsvol)-1,'市电状态'] = '停电'
            elif df_btsvol.loc[len(df_btsvol)-1,'直流电压'] -df_btsvol.loc[len(df_btsvol)-2,'直流电压'] >= 0.3: 
                df_btsvol.loc[len(df_btsvol)-1,'市电状态'] = '来电'
    
        for j in range(0,len(df_btsvol)-1,1):
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
            if time.strptime(break_time[0],'%Y-%m-%d %H:%M:%S') > time.strptime(resume_time[0],'%Y-%m-%d %H:%M:%S'):
                resume_time.pop(0)  #如果第一次停电时间比第一次恢复时间还晚，则说明停电时间发生在更早，则第一次恢复时间无意思，删除        
            lis_tmp=[] 
            for k in range(0,len(break_time),1):
                if time.strptime(break_time[k],'%Y-%m-%d %H:%M:%S') > time.strptime(resume_time[len(resume_time)-1],'%Y-%m-%d %H:%M:%S'):
                    lis_tmp.append(break_time[k])  # 找出时间晚于最后一次恢复时间的所欲停电，可以视为都是一次停电
                    for m in range(1,len(lis_tmp),1):
                        break_time.remove(lis_tmp[m]) # 保留最早的一条，其余可视为重复记录删除                        
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
        
        # =============================================================================
        #   注意这里有个大坑，如果通过循环遍历删除list：break_time中的元素，list后面的元素会自动向上补位，导致循环报错
        #   所有需要复制一份list的副本作为循环的条件，然后删除原list中的值。或者倒序删除                    
        # =============================================================================
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
          
    current_time = str(datetime.now()).split('.')[0]
    current_time = current_time.replace(':','.')
    
    writer = pd.ExcelWriter(out_path + current_time + '_4G基站停电.xls')
    df_power_down.to_excel(writer,current_time + '_停电') 
    df_vol.to_excel(writer,current_time + '_原始数据') 
    writer.save()
        




