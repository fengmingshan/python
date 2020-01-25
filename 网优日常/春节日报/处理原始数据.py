# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 15:03:09 2020

@author: Administrator
"""

import time
import streamlit as st
from datetime import datetime
import numpy as np
import pandas as pd
import os
import sched
import shutil
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


sche = sched.scheduler(time.time, time.sleep)
path = 'D:/Test/春节日报'
os.chdir(path)

df_enodeb_name = pd.read_excel('./物理站址清单.xlsx', encoding='utf-8')
PRB_titles = ['DATE_ID','HOUR_ID', 'eNodeB', 'EUTRANCELLFDD', 'Acc_Wireless ConnSucRate(%)', 'Acc_ERAB_dropping rate (%)', 'Air Interface_Traffic_Volume_UL_MBytes', 'Air Interface_Traffic_Volume_DL_MBytes', 'DL user timer(ms)', 'DL_Util_of_PRB', 'pmCellDowntimeAuto1', 'pmCellDowntimeMan1', 'Data_Coverage', 'Max number of UE in RRc', 'Avg Number of UL Active Users', 'Avg Number of DL Active Users', 'Max Number of DL Active Users', 'Max Number of UL Active Users', 'Avg User Fell Throughput (Mbps)'
              ]


files_4G = os.listdir('./原始数据')
if len(files_4G) > 0:  # 调用sche实力的enter方法创建一个定时任务，1800秒之后执行，#任务内容执行task()函数
    zte_4G_files = []
    eric_4G_files = []
    for file in files_4G:
        df = pd.read_csv('./原始数据/' + file, engine='python', encoding='gbk', nrows=1)
        if '子网名称' in df.columns:
            zte_4G_files.append(file)
        elif '2020' in df.columns[0]:
            eric_4G_files.append(file)
    # =============================================================================
    # #中兴数据处理
    # =============================================================================
    df_zte_4G = pd.DataFrame()
    for file in zte_4G_files:
        df_tmp = pd.read_csv('./原始数据/' + file, engine='python', encoding='gbk')
        df_tmp.fillna(0, inplace=True)
        df_tmp['日期'] = df_tmp['开始时间'].map(lambda x: str(x).split(' ')[0])
        df_tmp['时间'] = df_tmp['开始时间'].map(lambda x: float(str(x).split(' ')[1].split(':')[0]))
        df_tmp['小区号'] = df_tmp['网元'].map(str) + '_' + df_tmp['小区'].map(str)
        df_tmp['空口上行用户面流量（MByte）_1'] = df_tmp['空口上行用户面流量（MByte）_1'].map(
            lambda x: float(x.replace(',', '')))
        df_tmp['空口下行用户面流量（MByte）_1477070755617-11'] = df_tmp['空口下行用户面流量（MByte）_1477070755617-11'].map(
            lambda x: float(x.replace(',', '')))
# a=list(df_tmp.columns)
# print(a)
        df_tmp.rename(columns={'空口上行用户面流量（MByte）_1': '上行流量(GB)',
                               '空口下行用户面流量（MByte）_1477070755617-11': '下行流量(GB)',
                               '分QCI用户体验下行平均速率（Mbps）_1': '体验速率',
                               '最大RRC连接用户数_1': '用户数',
                               '下行PRB平均占用率_1': 'PRB利用率'}, inplace=True)
        df_tmp['上行流量(GB)'] = round(df_tmp['上行流量(GB)'] / 1024, 2)
        df_tmp['下行流量(GB)'] = round(df_tmp['下行流量(GB)'] / 1024, 2)
        df_tmp['总流量(GB)'] = round(df_tmp['上行流量(GB)'] + df_tmp['下行流量(GB)'], 2)
        df_tmp = df_tmp[['日期', '时间', '网元', '小区号', '小区名称', '用户数','总流量(GB)','体验速率','PRB利用率']]
        df_tmp = pd.merge(df_tmp, df_enodeb_name, how='left', on = '小区号')
        df_zte_4G = df_zte_4G.append(df_tmp)

# =============================================================================
# #爱立信PRB数据处理
# =============================================================================
    df_eric_4G = pd.DataFrame()
    for file in eric_4G_files:
        df_tmp = pd.read_csv('./原始数据/'+ file, header=None, names = PRB_titles, engine = 'python', encoding = 'gbk')
        df_tmp.fillna(0, inplace=True)
        df_tmp['DATE_ID'] = df_tmp['DATE_ID'].map(lambda x: x.replace('\'', ''))
        df_tmp['eNodeB'] = df_tmp['eNodeB'].map(lambda x: x.replace('\'', ''))
        df_tmp['EUTRANCELLFDD'] = df_tmp['EUTRANCELLFDD'].map(lambda x: x.replace('\'', ''))
        df_tmp['小区号'] = df_tmp['eNodeB'].map(lambda x: x.replace(
           '\'', '')) + '_' + df_tmp['EUTRANCELLFDD'].map(lambda x: x.split('_')[1])
        # a=list(df_tmp.columns)
        # print(a)
        df_tmp.rename(columns={'eNodeB': '网元',
                               'EUTRANCELLFDD': '小区名称',
                               'DATE_ID': '日期',
                               'HOUR_ID': '时间',
                               'Max number of UE in RRc': '用户数',
                               'DL_Util_of_PRB': 'PRB利用率',
                               'Avg User Fell Throughput (Mbps)': '体验速率',
                               'Air Interface_Traffic_Volume_UL_MBytes': '上行流量(GB)',
                               'Air Interface_Traffic_Volume_DL_MBytes': '下行流量(GB)'}, inplace=True)
        df_tmp['上行流量(GB)'] = round(df_tmp['上行流量(GB)'] / 1024, 2)
        df_tmp['下行流量(GB)'] = round(df_tmp['下行流量(GB)'] / 1024, 2)
        df_tmp['总流量(GB)'] = round(df_tmp['上行流量(GB)'] + df_tmp['下行流量(GB)'], 2)
        df_tmp = df_tmp[['日期', '时间', '网元', '小区号', '小区名称', '用户数','总流量(GB)','体验速率','PRB利用率']]
        df_tmp = pd.merge(df_tmp, df_enodeb_name, how='left', on = '小区号')
        df_eric_4G = df_eric_4G.append(df_tmp)

    df_总表 = df_zte_4G.append(df_eric_4G)
    df_总表['PRB利用率'] = df_总表['PRB利用率'].map(lambda x: float(str(x).split('%')[0]))

    df_country_flow = df_总表.groupby(by=['区县', '时间'])['总流量(GB)'].sum()
    df_country_flow = df_country_flow.reset_index()
    df_country_flow.sort_values(by ='时间',ascending = True, inplace=True)

    df_country_users = df_总表.groupby(by=['区县', '时间'])['总流量(GB)'].sum()
    df_country_users = df_country_users.reset_index()
    df_country_users.sort_values(by ='时间',ascending = True, inplace=True)

    df_suboffice_flow = df_总表.groupby(by=['区县', '支局', '时间'])['总流量(GB)'].sum()
    df_suboffice_flow = df_suboffice_flow.reset_index()
    df_suboffice_flow.sort_values(by ='时间',ascending = True, inplace=True)

    df_suboffice_uesr = df_总表.groupby(by=['区县', '支局', '时间'])['用户数'].sum()
    df_suboffice_uesr = df_suboffice_uesr.reset_index()
    df_suboffice_uesr.sort_values(by ='时间',ascending = True, inplace=True)

    df_BTS_flow = df_总表.groupby(by=['区县', '支局', '中文站名'])['总流量(GB)'].sum()
    df_BTS_flow = df_BTS_flow.reset_index()
    df_BTS_flow.sort_values(by ='总流量(GB)',ascending = False, inplace=True)

    df_pivot_hour = df_总表.groupby(by='时间')['用户数'].sum()
    df_pivot_hour.sort_values(ascending=False, inplace=True)
    df_pivot_hour = df_pivot_hour.reset_index()
    user_busy_hour = df_pivot_hour.时间.head(1).values[0]

    df_pivot_hour = df_总表.groupby(by='时间')['总流量(GB)'].sum()
    df_pivot_hour.sort_values(ascending=False, inplace = True)
    df_pivot_hour = df_pivot_hour.reset_index()
    flow_busy_hour = df_pivot_hour.时间.head(1).values[0]

    df_suboffice_user_busy = df_总表[df_总表.时间 == user_busy_hour]
    df_suboffice_user_busy = df_suboffice_user_busy.groupby(by=['区县', '支局'])['用户数'].sum()
    df_suboffice_user_busy = df_suboffice_user_busy.reset_index()
    df_suboffice_user_busy.sort_values(by ='用户数',ascending = False, inplace=True)

    df_suboffice_flow_day = df_总表.groupby(by=['区县', '支局'])['总流量(GB)'].sum()
    df_suboffice_flow_day = df_suboffice_flow_day.reset_index()
    df_suboffice_flow_day.sort_values(by ='总流量(GB)',ascending = False, inplace=True)

    df_user_busy = df_总表[df_总表.时间 == user_busy_hour]
    df_user_busy = df_user_busy.groupby(by=['区县', '支局', '中文站名'])['用户数'].sum()
    df_user_busy = df_user_busy.reset_index()
    df_user_busy.sort_values(by ='用户数',ascending = False, inplace=True)


    df_flow_busy = df_总表[df_总表.时间 == user_busy_hour]
    df_flow_busy = pd.pivot_table(df_flow_busy, index=['区县', '支局', '中文站名'],
                                  values=['总流量(GB)', 'PRB利用率', '体验速率'],
                                  aggfunc={'总流量(GB)': np.sum,
                                           'PRB利用率': np.max,
                                           '体验速率': np.mean
                                           })
    df_flow_busy.reset_index(inplace=True)

    with pd.ExcelWriter('节日原始数据.xlsx') as writer:
        df_country_flow.to_excel(writer, 'country_flow', index=False)
        df_country_users.to_excel(writer, 'country_user', index=False)
        df_suboffice_flow.to_excel(writer, 'suboffice_flow', index=False)
        df_suboffice_uesr.to_excel(writer, 'suboffice_uesr', index=False)
        df_user_busy.to_excel(writer, 'user_busy', index=False)
        df_flow_busy.to_excel(writer, 'flow_busy', index=False)
        df_BTS_flow.to_excel(writer, 'bts_flow', index=False)
        df_suboffice_user_busy.to_excel(writer, 'suboffice_user_busy', index=False)
        df_suboffice_flow_day.to_excel(writer, 'suboffice_flow_day', index=False)

    for file in files_4G:
        shutil.move('./原始数据/' + file, './原始数据_bak/' + file)
