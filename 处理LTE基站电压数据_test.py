# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 09:58:45 2018

@author: Administrator
"""
import os
import pandas as pd 
import time

#==============================================================================
# 获取当前日期
#==============================================================================
data_array=time.ctime(time.time()) # 获取当前时间
today = data_array[4:7]+'-'+data_array[8:10]  # 获取当前日期 格式为‘Mar-14’
sheet_time = data_array[11:13]+'点'+ data_array[14:16]+'分' # 获取表格生成的时间
data_trans = {'Jan':'1月','Feb':'2月','Mar':'3月','Apr':'4月','May':'5月','June':'6月',
              'July':'7月','Aug':'8月','Sept':'9月','Oct':'10月','Nov':'11月','Dec':'12月'} # 中英文月份对照字典
month = data_trans[today[0:3]]  # 将月份翻译为中文 
#month_day = month + today[4:6]+'日'  # 构建当天日期格式为 '3月14日'
month_day = '3月12日'

voltage_path =r'D:\4G_voltage'+'\\'
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
                    start_time.insert(0,' ')
                elif  time.strptime(end_time[len(end_time)-1],'%Y/%m/%d %H:%M:%S') < time.strptime(start_time[len(start_time)-1],'%Y/%m/%d %H:%M:%S'):
                    end_time.append(' ')
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
            
    writer = pd.ExcelWriter(voltage_path + month_day + sheet_time + '基站断站及停电.xls')
    df_power_down.to_excel(writer,sheet_time + '_停电') 
    df_vol.to_excel(writer,'原始记录') 
    writer.save()
    

    




