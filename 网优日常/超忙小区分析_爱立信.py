# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:06:25 2019

@author: Administrator
"""
import pandas as pd
import os
import numpy as np
from numba import jit
from math import ceil

data_path = r'd:/_小程序/超忙小区分析'
eric_file = '爱立信2019-09忙时.csv'
eric_cell_info = 'eric_cell_info.xlsx'
os.chdir(data_path)

df_cell_info = pd.read_excel(eric_cell_info)
df_cell_info.drop_duplicates('eNBId',keep ='first',inplace =True)
df_cell_info.set_index('eNBId',inplace =True)
cell_info_dict = df_cell_info['Site Name(Chinese)'].to_dict()

L1800_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 49, 50, 51, 52, 53, 54, 55,
    56, 129, 130, 131, 132, 133, 134, 135, 136, 177, 178, 179, 180, 181, 182]
L800_list = [17, 18, 19, 20, 21, 22, 145, 146, 147, 148, 149, 150]
title_list = ['DATE_ID',
              'HOUR_ID',
              'eNodeB',
              'EUTRANCELLFDD',
              'Acc_Wireless ConnSucRate(%)',
              'Acc_ERAB_dropping rate (%)',
              'Air Interface_Traffic_Volume_UL_MBytes',
              'Air Interface_Traffic_Volume_DL_MBytes',
              'Int_Downlink Latency (ms)',
              'Max number of UE in RRc', 'DL_Util_of_PRB',
              'pmCellDowntimeAuto1', 'pmCellDowntimeMan1', 'Data_Coverage',
              'Ava_CellAvail (%)', 'Num of LTE Redirect to 3G',
              'Avg Number of UL Active Users', 'Avg Number of DL Active Users',
              'Avg User Fell Throughput(Mbps)']

@jit()
def read_csv_block(file_name):
    file_content = pd.read_csv(
        file_name,
        engine='python',
        names = title_list,
        chunksize=10000)
    df_content = pd.DataFrame()
    i = 1
    for df_tmp in file_content:
        df_content = df_content.append(df_tmp)
        if i % 10 == 0:
            print('Finished: ', i ,'万行')
        i += 1
    return df_content

df_eric = read_csv_block(eric_file)
df_eric.columns = title_list

df_eric['Total_throughput'] = round(
    ((df_eric['Air Interface_Traffic_Volume_UL_MBytes'] +
      df_eric['Air Interface_Traffic_Volume_DL_MBytes']) /
     1024),
    2)
df_eric['Air Interface_Traffic_Volume_UL_MBytes'] = df_eric['Air Interface_Traffic_Volume_UL_MBytes'].map(
    lambda x: round(x / 1024, 2))
df_eric['Air Interface_Traffic_Volume_DL_MBytes'] = df_eric['Air Interface_Traffic_Volume_DL_MBytes'].map(
    lambda x: round(x / 1024, 2))
df_eric['week'] = pd.to_datetime(df_eric['DATE_ID'])
df_eric['week'] = df_eric['week'].map(lambda x: x.isocalendar()[1])

df_eric['cell'] = df_eric['EUTRANCELLFDD'].map(lambda x: x.split('_')[1])
df_eric['cell'] = df_eric['cell'].astype(int)

df_eric_L1800 = df_eric[df_eric['cell'].isin(L1800_list)]
df_eric_L800 = df_eric[df_eric['cell'].isin(L800_list)]

df_high_Data_800 = df_eric_L800[(df_eric_L800['Total_throughput'] >= 1.5) & (
    df_eric_L800['DL_Util_of_PRB'] >= 0.5)]
df_massive_users_800 = df_eric_L800[(df_eric_L800['Max number of UE in RRc'] >= 50) & (
    df_eric_L800['DL_Util_of_PRB'] >= 0.5)]

df_busy_cell_800 = df_high_Data_800.append(df_massive_users_800)

df_res_800 = pd.DataFrame()
for week in list(set(df_busy_cell_800['week'])):
    df_800 = df_busy_cell_800[df_busy_cell_800['week'] == week]
    # 按天进行透视，找出当天的最忙时
    df_pivot_800 = pd.pivot_table(
        df_800,
        index=[
            'DATE_ID',
            'eNodeB',
            'EUTRANCELLFDD',
            'week'],
        values=[
            'Total_throughput',
            'DL_Util_of_PRB',
            'Max number of UE in RRc',
            'Avg Number of DL Active Users',
            'Avg User Fell Throughput(Mbps)',
            'Air Interface_Traffic_Volume_UL_MBytes',
            'Air Interface_Traffic_Volume_DL_MBytes',
            'Int_Downlink Latency (ms)'],
        aggfunc={
            'Total_throughput': np.max,
            'DL_Util_of_PRB': np.max,
            'Max number of UE in RRc': np.max,
            'Avg Number of DL Active Users': np.max,
            'Avg User Fell Throughput(Mbps)': np.min,
            'Air Interface_Traffic_Volume_UL_MBytes': np.max,
            'Air Interface_Traffic_Volume_DL_MBytes': np.max,
            'Int_Downlink Latency (ms)': np.max})
    df_pivot_800 = df_pivot_800.reset_index()

    # 按周进行透视，求出本周平均值
    df_busy_day_count_800 = pd.pivot_table(
        df_pivot_800,
        index=[
            'eNodeB',
            'EUTRANCELLFDD',
            'week'],
        values=[
            'DATE_ID',
            'Total_throughput',
            'DL_Util_of_PRB',
            'Max number of UE in RRc',
            'Avg Number of DL Active Users',
            'Avg User Fell Throughput(Mbps)',
            'Air Interface_Traffic_Volume_UL_MBytes',
            'Air Interface_Traffic_Volume_DL_MBytes',
            'Int_Downlink Latency (ms)'],
        aggfunc={
            'DATE_ID': len,
            'Total_throughput': np.mean,
            'DL_Util_of_PRB': np.mean,
            'Max number of UE in RRc': np.mean,
            'Avg Number of DL Active Users': np.mean,
            'Avg User Fell Throughput(Mbps)': np.mean,
            'Air Interface_Traffic_Volume_UL_MBytes': np.mean,
            'Air Interface_Traffic_Volume_DL_MBytes': np.mean,
            'Int_Downlink Latency (ms)': np.mean})
    df_busy_day_count_800 = df_busy_day_count_800.reset_index()
    df_busy_day_count_800 = df_busy_day_count_800[df_busy_day_count_800['DATE_ID'] >= 4]
    df_busy_day_count_800.drop_duplicates(
        'EUTRANCELLFDD', keep='first', inplace=True)
    df_res_800 = df_res_800.append(df_busy_day_count_800)

df_res_800.sort_values(by='eNodeB', ascending=False, inplace=True)  # 按时间顺序降序排列

# 按扇区进行透视，计算出每个月出现超忙的周数
df_res_800 = pd.pivot_table(
    df_res_800,
    index=[
        'eNodeB',
        'EUTRANCELLFDD'],
    values=[
        'week',
        'Total_throughput',
        'DL_Util_of_PRB',
        'Max number of UE in RRc',
        'Avg Number of DL Active Users',
        'Avg User Fell Throughput(Mbps)',
        'Air Interface_Traffic_Volume_UL_MBytes',
        'Air Interface_Traffic_Volume_DL_MBytes',
        'Int_Downlink Latency (ms)'],
    aggfunc={
        'week': len,
        'Total_throughput': np.mean,
        'DL_Util_of_PRB': np.mean,
        'Max number of UE in RRc': np.mean,
        'Avg Number of DL Active Users': np.mean,
        'Avg User Fell Throughput(Mbps)': np.mean,
        'Air Interface_Traffic_Volume_UL_MBytes': np.mean,
        'Air Interface_Traffic_Volume_DL_MBytes': np.mean,
        'Int_Downlink Latency (ms)': np.mean})

df_res_800.rename(
    columns={
        'week': '超忙周数',
        'Total_throughput': '扇区忙时总流量_GB',
        'DL_Util_of_PRB': 'PRB利用率_%',
        'Max number of UE in RRc': 'RRC连接用户数',
        'Avg Number of DL Active Users': '下行激活用户数',
        'Avg User Fell Throughput(Mbps)': '用户体验速率_Mbps',
        'Air Interface_Traffic_Volume_UL_MBytes': '上行流量_GB',
        'Air Interface_Traffic_Volume_DL_MBytes': '下行流量_GB',
        'Int_Downlink Latency (ms)': '下行用户面时延_ms'},
    inplace = True)
df_res_800.reset_index(inplace = True)
df_res_800.drop_duplicates('EUTRANCELLFDD', keep = 'first', inplace = True)

# 处理数据格式
df_res_800['eNodeB']=df_res_800['eNodeB'].map(
    lambda x: x.replace('’'，'')
df_res_800['country']=df_res_800['EUTRANCELLFDD'].map(
    lambda x: x.split('QJ')[1][:2])
df_res_800['RRC连接用户数']=df_res_800['RRC连接用户数'].map(
    lambda x: ceil(x))
df_res_800['下行激活用户数']=df_res_800['下行激活用户数'].map(
    lambda x: ceil(x))
df_res_800['下行用户面时延_ms']=df_res_800['下行用户面时延_ms'].map(
    lambda x: round(x,0))
df_res_800['扇区忙时总流量_GB']=df_res_800['扇区忙时总流量_GB'].map(
    lambda x: round(x,2))
df_res_800['下行流量_GB']=df_res_800['下行流量_GB'].map(
    lambda x: round(x,2))
df_res_800['上行流量_GB']=df_res_800['上行流量_GB'].map(
    lambda x: round(x,2))
df_res_800['用户体验速率_Mbps']=df_res_800['用户体验速率_Mbps'].map(
    lambda x: round(x,2))
df_res_800['PRB利用率_%']=df_res_800['PRB利用率_%'].map(
    lambda x: round(x,2) if x<1 else 1)
df_res_800['扇区中文名'] = df_res_800['eNodeB'].map(cell_info_dict)

df_country_800= pd.pivot_table(df_res_800, index=['country'],
                                values = ['EUTRANCELLFDD'],
                                aggfunc = {'EUTRANCELLFDD': 'count'})
df_country_800=df_country_800.reset_index()

with pd.ExcelWriter('爱立信超忙小区.xlsx') as writer:  # 输出到excel
    df_res_800.to_excel(writer, 'L800超忙小区', index = False)
    df_country_800.to_excel(writer, '800M超忙按县统计', index = False)
