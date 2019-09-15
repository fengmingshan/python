# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:01:06 2019

@author: Administrator
"""

import pandas as pd
import os
from numpy import int64

data_path = 'd:/Test/存量3G用户数提取'

if not os.path.exists(data_path):
    os.mkdir(data_path)

os.chdir(data_path)

QJ_4G_record = 'qujing_rmk1_temp_20190903.csv'
QJ_billing_file = '划小清单201908.csv'

df_billing = pd.read_csv(QJ_billing_file,engine='python')

record_data = pd.read_csv(QJ_4G_record,engine = 'python',encoding = 'utf-8',  chunksize = 10000)
df_4G_record = pd.DataFrame()
i = 0
for df_tmp in record_data:
    i += 1
    try:
        df_4G_record = df_4G_record.append(df_tmp)
    except:
        print("Iteration is stopped.")
    if i%100 == 0:
        print('finished:{} lines.'.format(i*10000))

df_billing = df_billing[~df_billing['用户号码'].map(
    lambda x:str(x)[:4] == '0874' or str(x)[:3] == '874')]
df_billing['用户号码'] = df_billing['用户号码'].astype(int64)
df_billing = df_billing[['用户号码', '通话次数', '通话时长', '上网流量', '上网时长', '上网次数']]

df_only_3G = df_billing[~df_billing['用户号码'].isin(df_4G_record['rmk1'])]

df_only_3G['上网流量'] = df_only_3G['上网流量'].map(lambda x:round(x/(1024*1024)))
df_only_3G['日均流量'] = round(df_only_3G['上网流量']/30,0)
df_only_3G['平均网速'] = round(df_only_3G['上网流量']*1024/df_only_3G['上网时长'],0)

def judge_uesr_type(voice, data, avg_data):
    user_info_list = []
    if (voice == 0) & (data == 0):
        uesr_type = '双零用户'
        uesr_level = '无'
    elif (voice < 3) & (data > 0) & (avg_data < 30):
        uesr_type = '数据卡用户'
        uesr_level = '轻度'
    elif (voice < 3) & (data > 0) & (avg_data >= 30):
        uesr_type = '数据卡用户'
        uesr_level = '重度'
    elif (data >= 0) & (data < 100): # 100M流量
        uesr_type = '纯语音用户'
        uesr_level = '无'
    elif (voice >= 3) & (data > 100) & (avg_data < 30):
        uesr_type = '语音数据用户'
        uesr_level = '轻度'
    elif (voice >= 3) & (data > 100) & (avg_data >= 30):
        uesr_type = '语音数据用户'
        uesr_level = '重度'
    else:
        uesr_type = '无'
        uesr_level = '无'
    return (uesr_type, uesr_level)

df_only_3G['uesr_type'] = df_only_3G.apply(lambda x:judge_uesr_type(x.通话次数,x.上网流量,x.日均流量)[0],axis =1)
df_only_3G['uesr_level'] = df_only_3G.apply(lambda x:judge_uesr_type(x.通话次数,x.上网流量,x.日均流量)[1],axis =1)

df_3G_data_uesr =df_only_3G[df_only_3G['uesr_level'] == '重度']

with pd.ExcelWriter('存量纯3G用户清单.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_only_3G.to_excel(writer,'存量纯3G用户',index = False)
    df_3G_data_uesr.to_excel(writer,'3G重度数据用户',index = False)






