# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 09:58:45 2018

@author: Administrator
"""
import os
import pandas as pd 
from datetime import datetime
from datetime import timedelta
from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing import freeze_support

# =============================================================================
# 设置环境变量
# =============================================================================
data_path = r'C:\Users\Administrator\Desktop\3月发电核对\2018-03'+'\\'
out_path = r'C:\Users\Administrator\Desktop\3月发电核对'+'\\'
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
yestoday = '2018-03-27'

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


df_eNodeB_name = pd.read_excel(out_path +eNodeB_name ,encoding='utf-8') 
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

def collect_voinfo(file):
    collect_time = get_data_info(file)  # 通过文件名提取时间信息
    with open(data_path + file,'r',encoding='gbk') as file_tmp:
        content = file_tmp.readlines() 
        df_tmp = pd.DataFrame(columns=['eNodeB','直流电压','采集时间'])
        for i in range(0,len(content)-5,1):            
            if 'NE=' in  content[i] and 'PM单板诊断测试' in  content[i+5]:
                df_tmp.loc[i,'eNodeB']= content[i].split(',')[1][3:]
                df_tmp.loc[i,'采集时间']= collect_time
                df_tmp.loc[i,'直流电压']= float(content[i+5].split('    ')[3].split(' ')[4][:-1])
    return df_tmp

def handle_files(file_list,df_ommb_name,):  
    n=0     # 编号表示当天的第几次采集
    df_tmp = pd.DataFrame(columns=['eNodeB','直流电压','采集时间'])   #零时表格用来汇总每次采集的几个数据
    df_OMMB = pd.DataFrame(columns=['eNodeB'])
    df_OMMB['eNodeB'] = df_ommb_name['eNodeB']
    for i in range(0,len(file_list)-2,1):        
        df_tmp = df_tmp.append(collect_voinfo(file_list[i]),ignore_index=True)
        # 计算两个采集文件的时间差
        time_interval = (datetime.strptime(get_data_info(file_list[i+1]),"%Y-%m-%d %H:%M:%S") 
                        - datetime.strptime(get_data_info(file_list[i]),"%Y-%m-%d %H:%M:%S")).seconds 
        if time_interval < 360: # 如果采集时间差小于360秒，则是同一次采集，把数据追加在一起
            df_tmp = df_tmp.append(collect_voinfo(file_list[i+1]),ignore_index=True)
        elif time_interval > 360: # 如果采集时间差大于360秒，本次采集结束，则数据汇总到最终结果中
            n += 1
            df_tmp = df_tmp.groupby(by='eNodeB',as_index=False)[['直流电压','采集时间']].max()
            df_tmp['eNodeB'] = df_tmp['eNodeB'].astype(int) 
            df_tmp = pd.merge(df_ommb_name,df_tmp,how='left',on = 'eNodeB') 
            df_OMMB['时间_%s' %str(n)] = df_tmp['采集时间']
            df_OMMB['电压_%s' %str(n)] = df_tmp['直流电压']
            df_tmp = pd.DataFrame(columns=['eNodeB','直流电压','采集时间'])
    return df_OMMB
         

if __name__ == '__main__':
    
    current_time = str(datetime.now()).split('.')[0]
    print('任务开始时间:',current_time)
    
    freeze_support()
    p = Pool(2)     # 创建进程池
    omm1 = p.apply_async(handle_files, args=(file_ommb1,df_ommb1_name))  # 添加一个进程处理ommb1
    omm2 = p.apply_async(handle_files, args=(file_ommb2,df_ommb2_name))  # 添加一个进程处理ommb2
    p.close()   # 关闭进程池，之后就不能添加新的进程了
    p.join()    # 如果有进程Pool，调用join前必须先调用close

    df1 = omm1.get()    # 使用get()函数获取进程函数返回的结果
    df2 = omm2.get()    # 使用get()函数获取进程函数返回的结果
    df_merge = pd.DataFrame()
    df_merge = df1.append(df2,ignore_index=True)
    df_merge = df_merge.fillna('-')
    df_merge = pd.merge(df_eNodeB_name,df_merge,how='left',on ='eNodeB')     
    current_time = str(datetime.now()).split(' ')[0]    

    with pd.ExcelWriter(out_path + yestoday + '_LTE基站电压.xls') as writer:
        df_merge.to_excel(writer,yestoday+'_LTE基站电压') 
    current_time = str(datetime.now()).split('.')[0]
    print('任务结束时间:',current_time)

