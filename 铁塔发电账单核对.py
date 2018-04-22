# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 14:34:23 2018
铁塔发电账单核对
@author: Administrator
"""
import pandas as pd 
import os
from datetime import datetime 
from datetime import timedelta

# =============================================================================
# 环境变量
# =============================================================================
data_path = r'd:\python' + '\\'
bill = '2018年2月电信发电（结算表）.xlsx'
break_2G = '3G_2月断站.xlsx'
break_3G = '4G_2月断站.xlsx'

#df_bill = pd.read_excel(data_path + bill,encoding='utf-8') 
#df_fadian = df_bill[['资源系统编码','对应电信网管站名','铁塔审核发电开始时间','铁塔审核发电结束时间']]

df_2G = pd.read_excel(data_path + break_2G,encoding='utf-8') 
df_3G = pd.read_excel(data_path + break_3G,encoding='utf-8') 

df_2G_RRU = df_2G[['RRU信息','发生时间','最后一次发生时间',]][(df_2G['告警描述']=='未探测到RTR。')&(df_2G['RRU信息']!=' ')]
df_2G_RRU['name'] = df_2G_RRU['RRU信息'].map(lambda x:x.split('=')[2].split(',')[0])
df_2G_RRU.rename(columns={'RRU信息':'info'},inplace =True)
df_2G_BBU =  df_2G[['物理位置','发生时间','最后一次发生时间',]][(df_2G['告警描述']=='BTS掉站。')&(df_2G['物理位置']!=' ')]
df_2G_BBU['name'] = df_2G_BBU['物理位置'].map(lambda x:x.split('[')[3].split(']')[0])
df_2G_BBU.rename(columns={'物理位置':'info'},inplace =True)
df_2G_break = df_2G_RRU.append(df_2G_BBU)
df_2G_break.rename(columns={'最后一次发生时间':'告警恢复时间'},inplace =True)

df_3G_break = df_3G[['网元','发生时间','告警恢复时间']]
df_3G_break['name'] = df_3G_break['网元'].map(lambda x:x.split('(')[0])
df_3G_break.rename(columns={'网元':'info'},inplace =True)

df_break = df_2G_break.append(df_3G_break)

with pd.ExcelWriter(data_path + '2月_断站汇总.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_break.to_excel(writer,'2月')