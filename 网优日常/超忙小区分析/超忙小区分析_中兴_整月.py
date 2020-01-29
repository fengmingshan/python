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

data_path = r'D:/_python小程序/超忙小区分析'
zte_file = '2019年10月中兴超忙.csv'
os.chdir(data_path)
L1800_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 49, 50, 51, 52, 53, 54, 55,
    56, 129, 130, 131, 132, 133, 134, 135, 136, 177, 178, 179, 180, 181, 182]
L800_list = [17, 18, 19, 20, 21, 22, 145, 146, 147, 148, 149, 150]

@jit()
def read_csv_block(file_name):
    file_content = pd.read_csv(
        file_name,
        engine='python',
        chunksize=10000)
    df_content = pd.DataFrame()
    i = 1
    for df_tmp in file_content:
        df_content = df_content.append(df_tmp)
        if i % 10 == 0:
            print('Finished: ', i ,'万行')
        i += 1
    return df_content

# 读取文件
df_zte = read_csv_block(zte_file)
df_zte['空口上行用户面流量（MByte）_1'] = df_zte['空口上行用户面流量（MByte）_1'].map(lambda x:str(x).replace(',',''))
df_zte['空口下行用户面流量（MByte）_1477070755617-11'] = df_zte['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:str(x).replace(',',''))
df_zte['下行PRB平均占用率_1'] = df_zte['下行PRB平均占用率_1'].map(lambda x:str(x).replace('%',''))
df_zte['空口上行用户面流量（MByte）_1'] = df_zte['空口上行用户面流量（MByte）_1'].astype(float)
df_zte['空口下行用户面流量（MByte）_1477070755617-11'] = df_zte['空口下行用户面流量（MByte）_1477070755617-11'].astype(float)
df_zte['下行PRB平均占用率_1'] = df_zte['下行PRB平均占用率_1'].astype(float)/100
df_zte['小区总流量(GB)'] = round(((df_zte['空口上行用户面流量（MByte）_1']
                         + df_zte['空口下行用户面流量（MByte）_1477070755617-11'])/1024),2)
df_zte['小时'] = df_zte['开始时间'].map(lambda x:str(x).split(' ')[1][:2])
df_zte['日期'] = df_zte['开始时间'].map(lambda x:str(x).split(' ')[0])
df_zte['周'] =pd.to_datetime(df_zte['日期'])
df_zte['周'] = df_zte['周'].map(lambda x:x.isocalendar()[1])

df_zte = df_zte[df_zte['小区名称'].str.contains('_')]
df_zte['Net_type'] = df_zte['小区名称'].map(lambda x:x.split('_')[1])
df_zte['Net_type'] = df_zte['Net_type'].astype(int)

df_zte_L1800 = df_zte[df_zte['Net_type'].isin(L1800_list)]
df_zte_L800 = df_zte[df_zte['Net_type'].isin(L800_list)]

# 筛选1800M超忙扇区
df_high_Data_Volume = df_zte_L1800[(df_zte_L1800['小区总流量(GB)'] >= 6) & (df_zte_L1800['下行PRB平均占用率_1'] >= 0.5) ]
df_high_Data_Volume['超忙类别'] = '大流量'
df_massive_users = df_zte_L1800[(df_zte_L1800['最大RRC连接用户数_1'] >= 200) & (df_zte_L1800['下行PRB平均占用率_1'] >= 0.5) ]
df_massive_users['超忙类别'] = '多用户'
df_busy_cell_1800 = df_high_Data_Volume.append(df_massive_users)
df_busy_cell_1800['网络类别'] = '1800M'

# 筛选800M超忙扇区
df_high_Data_800 = df_zte_L800[(df_zte_L800['小区总流量(GB)'] >= 1.5) & (df_zte_L800['下行PRB平均占用率_1'] >= 0.5) ]
df_high_Data_800['超忙类别'] = '大流量'
df_massive_users_800 = df_zte_L800[(df_zte_L800['最大RRC连接用户数_1'] >= 50) & (df_zte_L800['下行PRB平均占用率_1'] >= 0.5) ]
df_massive_users_800['超忙类别'] = '多用户'
df_busy_cell_800 = df_high_Data_800.append(df_massive_users_800)
df_busy_cell_800['网络类别'] = '800M'

# 合并1800M和800M超忙小区
df_busy_cell  = df_busy_cell_1800.append(df_busy_cell_800)

df_res = pd.DataFrame()
for week in list(set(df_busy_cell['周'])):
    df_busy_week = df_busy_cell[df_busy_cell['周'] == week]
    # 按天进行透视，找出当天的最忙时
    df_pivot_day = pd.pivot_table(
        df_busy_week,
        index=[
            '日期',
            '网元',
            '小区名称',
            '周',
            '网络类别',
            '超忙类别'],
        values=[
            '小区总流量(GB)',
            '下行PRB平均占用率_1',
            '最大RRC连接用户数_1',
            '下行平均激活用户数_1',
            '最大激活用户数_1',
            '分QCI用户体验上行平均速率（Mbps）_1',
            '空口上行用户面流量（MByte）_1',
            '空口下行用户面流量（MByte）_1477070755617-11',
            '用户面下行包平均时延'],
        aggfunc={
            '小区总流量(GB)': np.max,
            '下行PRB平均占用率_1': np.max,
            '最大RRC连接用户数_1': np.max,
            '下行平均激活用户数_1': np.max,
            '最大激活用户数_1': np.max,
            '分QCI用户体验上行平均速率（Mbps）_1': np.min,
            '空口上行用户面流量（MByte）_1': np.max,
            '空口下行用户面流量（MByte）_1477070755617-11': np.max,
            '用户面下行包平均时延': np.max})
    df_pivot_day = df_pivot_day.reset_index()

    # 按周进行透视，求出本周平均值
    df_pivot_week = pd.pivot_table(
        df_pivot_day,
        index=[
            '网元',
            '小区名称',
            '周',
            '网络类别',
            '超忙类别'],
       values=[
            '日期',
            '小区总流量(GB)',
            '下行PRB平均占用率_1',
            '最大RRC连接用户数_1',
            '下行平均激活用户数_1',
            '最大激活用户数_1',
            '分QCI用户体验上行平均速率（Mbps）_1',
            '空口上行用户面流量（MByte）_1',
            '空口下行用户面流量（MByte）_1477070755617-11',
            '用户面下行包平均时延'],
        aggfunc={
            '日期':len,
            '小区总流量(GB)': np.mean,
            '下行PRB平均占用率_1': np.mean,
            '最大RRC连接用户数_1': np.mean,
            '下行平均激活用户数_1': np.mean,
            '最大激活用户数_1': np.mean,
            '分QCI用户体验上行平均速率（Mbps）_1': np.mean,
            '空口上行用户面流量（MByte）_1': np.mean,
            '空口下行用户面流量（MByte）_1477070755617-11': np.mean,
            '用户面下行包平均时延': np.mean})
    df_pivot_week = df_pivot_week.reset_index()
    df_pivot_week = df_pivot_week[df_pivot_week['日期'] >= 4]
    df_pivot_week.drop_duplicates(
        '小区名称', keep='first', inplace=True)
    df_res = df_res.append(df_pivot_week)

df_res.sort_values(by='网元', ascending=False, inplace=True)  # 按基站代码降序排列

# 按扇区进行透视，计算出每个月出现超忙的周数
df_res = pd.pivot_table(
    df_res,
        index=[
            '网元',
            '小区名称',
            '网络类别',
            '超忙类别'],
       values=[
            '周',
            '小区总流量(GB)',
            '下行PRB平均占用率_1',
            '最大RRC连接用户数_1',
            '下行平均激活用户数_1',
            '最大激活用户数_1',
            '分QCI用户体验上行平均速率（Mbps）_1',
            '空口上行用户面流量（MByte）_1',
            '空口下行用户面流量（MByte）_1477070755617-11',
            '用户面下行包平均时延'],
        aggfunc={
            '周' : len,
            '小区总流量(GB)': np.mean,
            '下行PRB平均占用率_1': np.mean,
            '最大RRC连接用户数_1': np.mean,
            '下行平均激活用户数_1': np.mean,
            '最大激活用户数_1': np.mean,
            '分QCI用户体验上行平均速率（Mbps）_1': np.mean,
            '空口上行用户面流量（MByte）_1': np.mean,
            '空口下行用户面流量（MByte）_1477070755617-11': np.mean,
            '用户面下行包平均时延': np.mean})

df_res.rename(
    columns={
        '周': '超忙周数',
        '小区总流量(GB)': '扇区忙时总流量_GB',
        '下行PRB平均占用率_1': 'PRB利用率_%',
        '最大RRC连接用户数_1': 'RRC连接用户数',
        '下行平均激活用户数_1': '平均激活用户数',
        '最大激活用户数_1': '最大激活用户数',
        '分QCI用户体验上行平均速率（Mbps）_1': '用户体验速率_Mbps',
        '空口上行用户面流量（MByte）_1': '上行流量_GB',
        '空口下行用户面流量（MByte）_1477070755617-11': '下行流量_GB',
        '用户面下行包平均时延': '下行用户面时延_ms'},
    inplace = True)
df_res.reset_index(inplace = True)
df_res.drop_duplicates('小区名称', keep = 'first', inplace = True)

# 处理数据格式
df_res['区县']=df_res['小区名称'].map(
    lambda x: x.split('QJ')[1][:2])
df_res['RRC连接用户数']=df_res['RRC连接用户数'].map(
    lambda x: ceil(x))
df_res['平均激活用户数']=df_res['平均激活用户数'].map(
    lambda x: ceil(x))
df_res['最大激活用户数']=df_res['最大激活用户数'].map(
    lambda x: ceil(x))
df_res['下行用户面时延_ms']=df_res['下行用户面时延_ms'].map(
    lambda x: round(x,0))
df_res['扇区忙时总流量_GB']=df_res['扇区忙时总流量_GB'].map(
    lambda x: round(x,2))
df_res['下行流量_GB']=df_res['下行流量_GB'].map(
    lambda x: round(x/1024,2))
df_res['上行流量_GB']=df_res['上行流量_GB'].map(
    lambda x: round(x/1024,2))
df_res['用户体验速率_Mbps']=df_res['用户体验速率_Mbps'].map(
    lambda x: round(x,2))
df_res['PRB利用率_%']=df_res['PRB利用率_%'].map(
    lambda x: round(x,2) if x<1 else 1)

# 按县透视超忙小区数量
df_country = pd.pivot_table(df_res, index=['区县'],
                                values = ['小区名称'],
                                aggfunc = {'小区名称': 'count'})
df_country = df_country.reset_index()

with pd.ExcelWriter('中兴超忙小区_结果输出.xlsx') as writer:  # 输出到excel
    df_res.to_excel(writer, '中兴超忙小区', index = False)
    df_country.to_excel(writer, '中兴超忙按县统计', index = False)
