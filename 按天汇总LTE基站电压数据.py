# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 09:58:45 2018

@author: Administrator
"""
import os
import pandas as pd 
from datetime import datetime
from datetime import timedelta

# =============================================================================
# 设置环境变量
# =============================================================================
data_path = r'D:\4G_voltage'+'\\'
out_path = r'D:\4G_voltage'+'\\'
eNodeB_name = 'eNode_name.xls'
yestoday = '2018-03-30'

#==============================================================================
# 定义获取当前时间信息的函数
#==============================================================================
def get_data_info(vofile):
    data_array = vofile.split('-')[3]
    time_array = vofile.split('-')[4] + vofile.split('-')[5][0:2]
    time_info = data_array[0:4] + '-' + data_array[4:6] + '-' + data_array[6:] + ' ' + time_array[0:2] + ':' + time_array[2:4] + ':' + time_array[4:]
    return time_info

#today = datetime.today()
#yestoday = today - timedelta(days=1)
#today = str(today).split(' ')[0]
#yestoday = str(yestoday).split(' ')[0]
yestoday = '2018-03-30'

all_files = os.listdir(data_path)
file_ommb1=[]
file_ommb2=[]
for vofile in all_files:
    if 'QJ_OMMB1' in vofile:
        if  get_data_info(vofile).split(' ')[0] == yestoday :
            file_ommb1.append(vofile)  # 找出昨天天采集的所有文件
    elif 'QJ_OMMB2' in vofile:
        if  get_data_info(vofile).split(' ')[0] == yestoday :
            file_ommb2.append(vofile)  # 找出昨天天采集的所有文件


df_eNodeB_name = pd.read_excel(data_path +eNodeB_name ,encoding='utf-8') 
df_eNodeB_name['区县'] = df_eNodeB_name['网元名称'].map(lambda x:x.split('QJ')[1][0:2])
df_OMMB1 =  df_eNodeB_name[df_eNodeB_name['网元名称'].str.contains('麒麟')|
                           df_eNodeB_name['网元名称'].str.contains('沾益')|
                           df_eNodeB_name['网元名称'].str.contains('马龙')|
                           df_eNodeB_name['网元名称'].str.contains('陆良')
]
df_OMMB2 =  df_eNodeB_name[df_eNodeB_name['网元名称'].str.contains('宣威')|
                           df_eNodeB_name['网元名称'].str.contains('会泽')|
                           df_eNodeB_name['网元名称'].str.contains('富源')|
                           df_eNodeB_name['网元名称'].str.contains('师宗')|
                           df_eNodeB_name['网元名称'].str.contains('罗平')
]
df_OMMB1 = df_OMMB1.reset_index()
df_OMMB2 = df_OMMB2.reset_index()
del df_OMMB1['index']
del df_OMMB2['index']

df_ommb1_name = df_OMMB1[['eNodeB']]    # 注意这里一定是双括号，如果是单括号，
df_ommb2_name = df_OMMB2[['eNodeB']]    # 取到的只是一列，而不是一个表，就不能进行merge等操作
df_result = pd.DataFrame(columns=['eNodeB','网元名称','区县'])
for i in range(0,48,1):
    df_OMMB1['时间_%s'% str(i+1)] =''
    df_OMMB1['电压_%s'% str(i+1)] =''
    df_OMMB2['时间_%s'% str(i+1)] =''
    df_OMMB2['电压_%s'% str(i+1)] =''
    df_result['时间_%s'% str(i+1)] =''
    df_result['电压_%s'% str(i+1)] =''
    
    
if len(file_ommb1) > 0:
    for i in range(0,len(file_ommb1),1):        
        collect_time = get_data_info(file_ommb1[i])  # 通过文件名提取时间信息
        file_tmp = open(data_path + file_ommb1[i],'r',encoding='gbk')  # 用零时文件读取原始记录文件
        content = file_tmp.readlines() 
        df_tmp1 = pd.DataFrame(columns=['eNodeB','直流电压','采集时间'])
        for j in range(0,len(content)-5,1):            
            if 'NE=' in  content[j] and 'PM单板诊断测试' in  content[j+5]:
                df_tmp1.loc[j,'eNodeB']= content[j].split(',')[1][3:]
                df_tmp1.loc[j,'采集时间']= collect_time
                df_tmp1.loc[j,'直流电压']= float(content[j+5].split('    ')[3].split(' ')[4][:-1])
        if len(df_tmp1) > 0 :
            df_tmp1 = df_tmp1.groupby(by='eNodeB',as_index=False)[['直流电压','采集时间']].max()
            df_tmp1['eNodeB'] =  df_tmp1['eNodeB'].astype(int) 
            df_tmp1 = pd.merge(df_ommb1_name,df_tmp1,how='left',on = 'eNodeB')              
            df_OMMB1['时间_%s' %str(i+1)] = df_tmp1['采集时间']
            df_OMMB1['电压_%s' %str(i+1)] = df_tmp1['直流电压']

if len(file_ommb2) > 0:
    for i in range(0,len(file_ommb2),1):        
        collect_time = get_data_info(file_ommb2[i])  # 通过文件名提取时间信息
        file_tmp = open(data_path + file_ommb2[i],'r',encoding='gbk')  # 用零时文件读取原始记录文件
        content = file_tmp.readlines() 
        df_tmp2 = pd.DataFrame(columns=['eNodeB','直流电压','采集时间'])
        for j in range(0,len(content)-5,1):            
            if 'NE=' in  content[j] and 'PM单板诊断测试' in  content[j+5]:
                df_tmp2.loc[j,'eNodeB']= content[j].split(',')[1][3:]
                df_tmp2.loc[j,'采集时间']= collect_time
                df_tmp2.loc[j,'直流电压']= float(content[j+5].split('    ')[3].split(' ')[4][:-1])                
        if len(df_tmp2) > 0 :
            df_tmp2 = df_tmp2.groupby(by='eNodeB',as_index=False)[['直流电压','采集时间']].max()
            df_tmp2['eNodeB'] =  df_tmp2['eNodeB'].astype(int)
            df_tmp2 = pd.merge(df_ommb2_name,df_tmp2,how='left',on = 'eNodeB')              
            df_OMMB2['时间_%s' %str(i+1)] = df_tmp2['采集时间']
            df_OMMB2['电压_%s' %str(i+1)] = df_tmp2['直流电压']
            
df_result = df_result.append(df_OMMB1,ignore_index=True)
df_result = df_result.append(df_OMMB2,ignore_index=True)  
      
current_time = str(datetime.now()).split(' ')[0]    
writer = pd.ExcelWriter(out_path + current_time + '_LTE基站电压.xls')
df_result.to_excel(writer,current_time+'_LTE基站电压') 
writer.save()
        
df_result = pd.read_excel(out_path +current_time + '_LTE基站电压.xls' ,encoding='utf-8') 
df_result = df_result.fillna('-')
writer = pd.ExcelWriter(out_path + current_time + '_LTE基站电压.xls')
df_result.to_excel(writer,current_time+'_LTE基站电压') 
writer.save()


