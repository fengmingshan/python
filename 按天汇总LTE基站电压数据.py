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

vo_files = os.listdir(data_path)
file_list=[]
for vofile in vo_files:
    if 'QJ_OMMB' in vofile:
        if  get_data_info(vofile).split(' ')[0] == yestoday :
            file_list.append(vofile)  # 找出昨天天采集的所有文件

df_eNodeB_name = pd.read_excel(data_path +eNodeB_name ,encoding='utf-8') 
df_one_day = pd.DataFrame(columns=['eNodeB','网元名称','区县'])
df_one_day['eNodeB'] = df_eNodeB_name['eNodeB']
df_one_day['网元名称'] = df_eNodeB_name['网元名称']
df_one_day['区县'] = df_eNodeB_name['网元名称'].map(lambda x:x.split('QJ')[1][0:2])

for i in range(0,48,1):
    df_one_day['时间_%s'% str(i+1)] =''
    df_one_day['电压_%s'% str(i+1)] =''

if len(file_list) > 0:
    for vofile_name in file_list:        
        collect_time = get_data_info(vofile_name)  # 通过文件名提取时间信息
        file_tmp = open(data_path + vofile_name,'r',encoding='gbk')  # 用零时文件读取原始记录文件
        content = file_tmp.readlines() 
        df_tmp = pd.DataFrame(columns=['eNodeB','直流电压','采集时间'])
        for i in range(0,len(content)-5,1):
            if 'NE=' in  content[i] and 'PM单板诊断测试' in  content[i+5]:
                df_tmp.loc[i,'eNodeB']= content[i].split(',')[1][3:]
                df_tmp.loc[i,'采集时间']= collect_time
                df_tmp.loc[i,'直流电压']= float(content[i+5].split('    ')[3].split(' ')[4][:-1])
        df_tmp = df_tmp.groupby(by='eNodeB',as_index=False)[['直流电压','采集时间']].max()
        df_tmp['eNodeB'] =  df_tmp['eNodeB'].astype(int)
        df_vol = pd.merge(df_eNodeB_name,df_tmp,how ='left',on ='eNodeB' )
              
    current_time = str(datetime.now()).split(' ')[0]
    
    writer = pd.ExcelWriter(out_path + current_time+'_BSC1基站电压.xls')
    df_bsc.to_excel(writer,current_time+'_4G电压') 
    writer.save()
        




