# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:06:25 2019

@author: Administrator
"""
import pandas as pd
import os
import numpy as np
from numba import jit

data_path = r'd:\_小程序\超忙小区分析' + '\\'
eric_file = r'爱立信2019-07忙时.csv'
L1800_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 49, 50, 51, 52, 53, 54, 55, 56, 129, 130, 131, 132, 133, 134, 135, 136, 177, 178, 179, 180, 181, 182]
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
              'Avg User Fell Throughput (Mbps)']

@jit()
def read_csv_block(file_name):
    file_content = pd.read_csv(
        file_name,
        engine='python',
        names=title_list,
        chunksize=10000)
    df_content = pd.DataFrame()
    i = 1
    for df_tmp in file_content:
        df_content = df_content.append(df_tmp)
        if i % 10 == 0:
            print('finished: ', i)
        i += 1
    return df_content

file_name = data_path + eric_file
df_eric = read_csv_block(file_name)
df_eric.columns = title_list

df_eric['Total_throughput'] = round(
    ((df_eric['Air Interface_Traffic_Volume_UL_MBytes'] +
      df_eric['Air Interface_Traffic_Volume_DL_MBytes']) /
     1024),
    2)

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
    df_pivot_800 = pd.pivot_table(
        df_800,
        index=[
            'DATE_ID',
            'eNodeB',
            'cell',
            'EUTRANCELLFDD',
            'week'],
        values=[
            'Total_throughput',
            'DL_Util_of_PRB',
            'Max number of UE in RRc'],
        aggfunc={
            'Total_throughput': np.max,
            'DL_Util_of_PRB': np.max,
            'Max number of UE in RRc': np.max})
    df_pivot_800 = df_pivot_800.reset_index()

    df_busy_day_count_800 = pd.pivot_table(
        df_pivot_800,
        index=[
            'eNodeB',
            'cell',
            'EUTRANCELLFDD',
            'week'],
        values=[
            'DATE_ID',
            'Total_throughput',
            'DL_Util_of_PRB',
            'Max number of UE in RRc'],
        aggfunc={
            'DATE_ID': len,
            'Total_throughput': np.max,
            'DL_Util_of_PRB': np.max,
            'Max number of UE in RRc': np.max})
    df_busy_day_count_800 = df_busy_day_count_800.reset_index()
    df_busy_day_count_800 = df_busy_day_count_800[df_busy_day_count_800['DATE_ID'] >= 4]
    df_busy_day_count_800.drop_duplicates(
        'EUTRANCELLFDD', keep='first', inplace=True)
    df_res_800 = df_res_800.append(df_busy_day_count_800)

df_res_800.sort_values(by='eNodeB', ascending=False, inplace=True)  # 按时间顺序降序排列

df_res_800 = pd.pivot_table(
    df_res_800,
    index=[
        'eNodeB',
        'cell',
        'EUTRANCELLFDD',
    ],
    values=[
        'week',
        'Total_throughput',
        'DL_Util_of_PRB',
        'Max number of UE in RRc'],
    aggfunc={
        'week': len,
        'Total_throughput': np.max,
        'DL_Util_of_PRB': np.max,
        'Max number of UE in RRc': np.max})
df_res_800.rename(
    columns={
        'week': 'busy_week_count',
        'Total_throughput': 'Total_throughput_GB'},
    inplace=True)
df_res_800.reset_index(inplace=True)
df_res_800.drop_duplicates('EUTRANCELLFDD', keep='first', inplace=True)
df_res_800['country'] = df_res_800['EUTRANCELLFDD'].map(
    lambda x: x.split('QJ')[1][:2])

df_country_800 = pd.pivot_table(df_res_800, index=['country'],
                                values=['EUTRANCELLFDD'],
                                aggfunc={'EUTRANCELLFDD': 'count'})
df_country_800 = df_country_800.reset_index()

with pd.ExcelWriter(data_path + '爱立信超忙小区.xlsx') as writer:  # 输出到excel
    df_res_800.to_excel(writer, 'L800超忙小区', index=False)
    df_country_800.to_excel(writer, '800M超忙按县统计', index=False)
