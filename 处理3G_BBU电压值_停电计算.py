# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 17:13:59 2018

@author: Administrator
"""
import pandas as pd
import os
from datetime import datetime
from datetime import timedelta
import time


data_path = r'd:\3G_voltage'+'\\' 
out_path = r'd:\3G_voltage'+'\\' 
bts_name = 'bts_name.xls'
df_bts = pd.read_excel(data_path + bts_name,dtype =str,encoding='utf-8') 
df_bts.rename(columns =({'bssid':'BSC','system':'基站号','btsalias': '名称'}), inplace=True)
df_bsc1 = df_bts[df_bts['BSC'] == 'BSC1']

def get_time_info(vofile):
    date_array = vofile.split('_')[1]
    time_array = vofile.split('_')[2][:6]
    time_info = date_array + ' '+ time_array[0:2] + ':' + time_array[2:4] + ':' + time_array[4:6]
    return time_info

#today = datetime.today()
#yestoday = today - timedelta(days=1)
#today =str(today).split(' ')[0]
#yestoday = str(yestoday).split(' ')[0]
today = '2018-03-26'
yestoday = '2018-03-27' 

all_files = os.listdir(data_path)
vo_file_list = []
for file in all_files:
    if '-fm-envi-info' in file:
        if (get_time_info(file).split(' ')[0] == today 
        or get_time_info(file).split(' ')[0] == yestoday):
            vo_file_list.append(file)

df_vol = pd.DataFrame(columns=['名称','系统号','BTS类型','输入电压(V)','更新时间'])

for i in range(0,len(vo_file_list),1):
    df_file = pd.read_table(data_path + vo_file_list[i],sep='\t',header=0,index_col=None,engine='python')  
    col_name = df_file.columns.map(lambda x:x.strip())  #将df_file列名中多余的空格去掉
    df_file.columns = col_name    
    df_file['BTS类型'] = df_file['BTS类型'].map(lambda x:x.strip())   #  将df_file['BTS类型']列中多余的空格去掉
    df_file['别名'] = df_file['别名'].map(lambda x:x.strip())   #  将df_file['别名']列中多余的空格去掉
    df_file = df_file[(df_file['BTS类型']!='CBTS I2')&(df_file['BTS类型']!='BTSB I4')]  # 不要 CBTS I2 和 BTSB I4                                                
    df_file['输入电压(V)'] = df_file['输入电压(V)'].map(lambda x:x.strip())     #  将 df_file['输入电压(V)']列中多余的空格去掉
    df_file['输入电压(V)'] = df_file['输入电压(V)'].map(lambda x:x.replace('---','0'))     #  将 df_file['输入电压(V)']列中多余的空格去掉
    df_file['输入电压(V)'] = df_file['输入电压(V)'].astype(float)   #  将 df_file['输入电压(V)']列转换成浮点数
    df_file = df_file[['系统号','BTS类型','别名','输入电压(V)','更新时间']]
    # 因为取电压值每个基站可能刷新了多条数据，所以通过groupby取电压的最大值
    df_file = df_file.groupby(by='别名',as_index=False)[['系统号','BTS类型','输入电压(V)','更新时间']].max() 
    df_file.rename(columns=({'别名':'名称'}), inplace=True)
    df_vol = df_vol.append(df_file,ignore_index=True)
    df_vol = df_vol.sort_values(by='更新时间',ascending = True) # 按时间顺序升序排列
    
df_low_power = df_vol[df_vol['输入电压(V)']<50]     # 筛选电池电压低于50v的基站，可能发生了停电
low_power_bts =  list(set(list(df_low_power['名称'])))  # 通过转换为set去重复
df_power_down = pd.DataFrame(columns=['名称','区县','系统号','当前电压',
        '市电状态','停电时间','持续时间','恢复时间','数据更新时间']) # 用来装停电计算结果

for i in range(0,len(low_power_bts),1):        
    df_btsvol = df_vol[df_vol['名称']== low_power_bts[i]]
    df_btsvol = df_btsvol.reset_index()
    df_btsvol['市电状态'] = ''
    if len(df_btsvol) >= 2 :
        if df_btsvol.loc[len(df_btsvol)-1,'输入电压(V)'] -df_btsvol.loc[len(df_btsvol)-2,'输入电压(V)'] <= -0.3:   #计算电压差，最后一行需要单独计算
            df_btsvol.loc[len(df_btsvol)-1,'市电状态'] = '停电'
        elif df_btsvol.loc[len(df_btsvol)-1,'输入电压(V)'] -df_btsvol.loc[len(df_btsvol)-2,'输入电压(V)'] >= 0.3: 
            df_btsvol.loc[len(df_btsvol)-1,'市电状态'] = '来电'

    for j in range(0,len(df_btsvol)-1,1):
        if df_btsvol.loc[j,'输入电压(V)'] - df_btsvol.loc[j+1,'输入电压(V)'] >= 0.3:      # 循环计算电压差，得到市电状态
            df_btsvol.loc[j,'市电状态'] = '停电'
        elif df_btsvol.loc[j,'输入电压(V)'] - df_btsvol.loc[j+1,'输入电压(V)'] <= -0.3:
            df_btsvol.loc[j,'市电状态'] = '来电'

    df_down_tmp = pd.DataFrame(columns=['名称','区县','系统号','当前电压',
        '市电状态','停电时间','持续时间','恢复时间','数据更新时间'])
    start_time = df_btsvol.loc[0,'更新时间']  
    end_time = df_btsvol.loc[len(df_btsvol)-1,'更新时间']     
    break_time = [] # 用来存储停电时间
    resume_time = [] # 用来存储恢复时间
    if df_btsvol.loc[0,'市电状态'] =='停电':
        break_time.append(start_time)
    for k in range(0,len(df_btsvol)-1,1):
        if df_btsvol.loc[k,'市电状态'] =='' and df_btsvol.loc[k+1,'市电状态'] =='停电' and df_btsvol.loc[k+1,'输入电压(V)'] < 55 :
            break_time.append(df_btsvol.loc[k+1,'更新时间'])
        elif df_btsvol.loc[k,'市电状态'] =='来电' and df_btsvol.loc[k+1,'市电状态'] =='停电' and df_btsvol.loc[k+1,'输入电压(V)'] < 55 :
            break_time.append(df_btsvol.loc[k+1,'更新时间'])
        elif df_btsvol.loc[k,'市电状态'] =='' and df_btsvol.loc[k+1,'市电状态'] =='来电' and df_btsvol.loc[k+1,'输入电压(V)'] <54:
            resume_time.append(df_btsvol.loc[k+1,'更新时间'])
        elif df_btsvol.loc[k,'市电状态'] =='停电' and df_btsvol.loc[k+1,'市电状态'] =='来电' and df_btsvol.loc[k+1,'输入电压(V)'] <54:
            resume_time.append(df_btsvol.loc[k+1,'更新时间'])

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

# =============================================================================
#   注意这里有个大坑，如果通过循环遍历删除list：break_time中的元素，list后面的元素会自动向上补位，导致循环报错
#   所有需要复制一份list的副本作为循环的条件，然后删除原list中的值。或者倒序删除                    
# =============================================================================
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
        df_down_tmp.loc[n,'名称'] = df_btsvol.loc[0,'名称']
        df_down_tmp.loc[n,'区县'] = df_btsvol.loc[0,'名称'].split('QJ')[1][0:2]
        df_down_tmp.loc[n,'系统号'] = df_btsvol.loc[0,'系统号']
        df_down_tmp.loc[n,'当前电压'] = df_btsvol.loc[len(df_btsvol)-1,'输入电压(V)']
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

with pd.ExcelWriter(out_path + current_time + '_3G基站停电.xls') as writer:
    df_power_down.to_excel(writer,current_time + '_停电') 
    #df_vol.to_excel(writer,'原始记录') 


