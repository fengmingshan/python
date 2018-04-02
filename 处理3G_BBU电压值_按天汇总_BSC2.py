# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 17:13:59 2018

@author: Administrator
"""
import pandas as pd
import os
from datetime import datetime
from datetime import timedelta


data_path = r'd:\3G_voltage'+'\\' 
out_path = r'd:\3G_voltage'+'\\' 
bts_name = 'bts_name.xls'
df_bts = pd.read_excel(data_path + bts_name,dtype =str,encoding='utf-8') 
df_bts.rename(columns =({'bssid':'BSC','system':'基站号','btsalias': '名称'}), inplace=True)
df_bsc2 = df_bts[df_bts['BSC'] == 'BSC2']
for i in range(0,48,1):
    df_bsc2['时间_%s'% str(i+1)] =''
    df_bsc2['电压_%s'% str(i+1)] =''


today = '2018-03-23'

def get_time_info(vofile):
    date_array = vofile.split('_')[1]
    time_array = vofile.split('_')[2][:6]
    time_info = date_array + ' '+ time_array[0:2] + ':' + time_array[2:4] + ':' + time_array[4:6]
    return time_info

#today = datetime.today()
#yestoday = today - timedelta(days=1)
#today =str(today).split(' ')[0]
#yestoday = str(yestoday).split(' ')[0]

all_files = os.listdir(data_path)
vo_file_list = []
for file in all_files:
    if '-fm-envi-info' in file:
        if get_time_info(file).split(' ')[0] == today:
            vo_file_list.append(file)

df_result = pd.DataFrame(columns=['别名','系统号','BTS类型','输入电压(V)','更新时间'])
df_vol = pd.DataFrame(columns=['别名','系统号','BTS类型','输入电压(V)','更新时间'])

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
    # 因为取电压值每个基站可能刷新了多条数据，所以通过groupby取电压最大值
    df_file = df_file.groupby(by='别名',as_index=False)[['系统号','BTS类型','输入电压(V)','更新时间']].max() 
    df_file.rename(columns=({'别名':'名称'}), inplace=True)
    df_tmp = pd.merge(df_bsc2,df_file,how = 'left',on = '名称' )
    #df_vol = df_vol.append(df_file,ignore_index=True)
    df_bsc2['时间_%s' %str(i+1)] = df_tmp['更新时间']
    df_bsc2['电压_%s' %str(i+1)] = df_tmp['输入电压(V)']

current_time = str(datetime.now()).split(' ')[0]
df_bsc2.to_excel(out_path + current_time+'_BSC2基站电压.xls',current_time+'_3G电压') # 写入到excel


