# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 11:13:20 2019

@author: Administrator
"""

import pandas as pd
import os
import numpy

data_path = 'D:/Notebook/CQI质差小区根因分析'
os.chdir(data_path)

all_files = os.listdir('./data')

mr_files = [x for x in all_files if 'MR' in x]
TA_files = [x for x in all_files if 'TA' in x]
CQI_files = [x for x in all_files if 'CQI' in x]
KPI_files = [x for x in all_files if 'KPI' in x]

df_mr = pd.DataFrame()
for file in mr_files:
    df_tmp = pd.read_csv('./data/' + file, engine='python')
    df_tmp = df_tmp[(df_tmp['区域'] == '曲靖市') & (df_tmp['厂家'] == '中兴')]
    df_mr = df_mr.append(df_tmp)
df_mr['cell_id'] = df_mr['NAME'].map(lambda x: x.split('_')[0] + '_' + x.split('_')[1])
df_mr['day_index'] = df_mr['时间周期'] + '_' + df_mr['cell_id']
df_mr = df_mr[['平均RSRP（dBm）', '|≥-105dBm采样点', '|≥-110dBm采样点',
               '|≥-115dBm采样点', '|≥-120dBm采样点', '|≥负无穷采样点', 'day_index']]

df_TA = pd.DataFrame()
for file in TA_files:
    df_tmp = pd.read_csv('./data/' + file, engine='python')
    df_TA = df_TA.append(df_tmp)
df_TA['cell_id'] = df_TA['eNodeB'].map(str) + '_' + df_TA['小区'].map(str)
df_TA['time_index'] = df_TA['开始时间'] + '_' + df_TA['cell_id']
df_TA['0.5km以下'] = df_TA['TA在范围[0,1)的上报次数'] + df_TA['TA在范围[1,3)的上报次数'] + \
    df_TA['TA在范围[3,5)的上报次数'] + df_TA['TA在范围[5,7)的上报次数']
df_TA['0.5km-1km'] = df_TA['TA在范围[7,9)的上报次数'] + df_TA['TA在范围[9,11)的上报次数'] + \
    df_TA['TA在范围[11,13)的上报次数']
df_TA['1km-1.5km'] = df_TA['TA在范围[13,20)的上报次数']
df_TA['1.5km-2.1km'] = df_TA['TA在范围[20,27)的上报次数']
df_TA['2.1km-3.1km'] = df_TA['TA在范围[27,34)的上报次数'] + df_TA['TA在范围[34,40)的上报次数']
df_TA['3.1km-3.9km'] = df_TA['TA在范围[40,50)的上报次数']
df_TA['3.9km-6.3km'] = df_TA['TA在范围[50,81)的上报次数']
df_TA['6.3km以上'] = df_TA['TA在范围[50,81)的上报次数']
df_TA = df_TA[['cell_id', 'time_index', '0.5km以下', '0.5km-1km', '1km-1.5km',
               '1.5km-2.1km', '2.1km-3.1km', '3.1km-3.9km', '3.9km-6.3km', '6.3km以上']]
df_KPI = pd.DataFrame()
for file in KPI_files:
    df_tmp = pd.read_csv('./data/' + file, engine='python')
    df_KPI = df_KPI.append(df_tmp)
df_KPI['cell_id'] = df_KPI['网元'].map(str) + '_' + df_KPI['小区'].map(str)
df_KPI['CQI>=7占比'] = df_KPI['CQI>=7占比'].map(lambda x: float(x.replace('%', '')))
df_KPI['time_index'] = df_KPI['开始时间'] + '_' + df_KPI['cell_id']
df_KPI = df_KPI[['time_index',
                 '空口下行用户面流量（MByte）_1477070755617-11',
                 '空口下行用户面丢包率_1',
                 '下行PRB平均占用率_1',
                 'PDCCH信道CCE占用率_1',
                 '平均RRC连接用户数_1',
                 '下行平均激活用户数_1',
                 'Total DL Data Volume(GB)',
                 'CQI优良比(>=7比例)',
                 'CQI>=7占比']]

df_all = pd.merge(df_KPI, df_TA, how='left', on='time_index')
df_all['day_index'] = df_all['time_index'].map(lambda x: x.split(' ')[0]) + '_' + df_all['cell_id']
df_all = pd.merge(df_all, df_mr, how='left', on='day_index')