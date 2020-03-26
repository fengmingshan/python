# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:05:31 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
import os


def zte_KPI_busy_rename(df):
    df.rename(columns={"RRC连接重建比例_1": "RRC连接重建比例",
                       "UE上下文掉线率_1": "UE上下文掉线率",
                       "RAB掉线率_1": "RAB掉线率",
                       "S1接口切换成功率_1": "S1接口切换成功率",
                       "系统内切换成功率_1": "系统内切换成功率",
                       "LTE重定向到3G的次数_1": "LTE重定向到3G的次数",
                       "空口上行用户面流量（MByte）_1": "上行流量_MB",
                       "空口下行用户面流量（MByte）_1477070755617-11": "下行流量_MB",
                       "分QCI用户体验上行平均速率（Mbps）_1": "上行体验速率_Mbps",
                       "分QCI用户体验下行平均速率（Mbps）_1": "下行体验速率_Mbps",
                       "空口下行用户面丢包率_1": "空口下行用户面丢包率",
                       "上行PRB平均占用率_1": "上行PRB平均占用率",
                       "下行PRB平均占用率_1": "下行PRB平均占用率",
                       "PDCCH信道CCE占用率_1": "PDCCH信道CCE占用率",
                       "PRACH信道占用率_1": "PRACH信道占用率",
                       "非竞争 Preamble占用率_1": "非竞争Preamble占用率",
                       "寻呼信道占用率_1": "寻呼信道占用率",
                       "最大RRC连接用户数_1": "最大RRC连接用户数",
                       "平均RRC连接用户数_1": "平均RRC连接用户数",
                       "上行平均激活用户数_1": "上行平均激活用户数",
                       "下行平均激活用户数_1": "下行平均激活用户数",
                       "平均激活用户数_1": "平均激活用户数",
                       "最大激活用户数_1": "最大激活用户数",
                       "CQI优良比(>=7比例)": "CQI优良比",
                       }, inplace=True
              )
    return df


work_path = 'D:/2020年工作/2020年3月5G规划'
os.chdir(work_path)

df_hour = pd.read_csv('2020_03_25_16_44_15_445_qj_wxzx_fengmingshan_忙时.csv',
                      engine='python', encoding='gbk')
df_hour = zte_KPI_busy_rename(df_hour)
df_hour['日期'] = df_hour['开始时间'].map(lambda x: x.split(' ')[0])
df_hour['小时'] = df_hour['开始时间'].map(lambda x: x.split(' ')[1])


df_group = df_hour.groupby(['日期', '网元', '网元名称', '小区', '小区名称'],
                           as_index=False)['下行流量_MB'].agg(np.max)
df_busy_hour = pd.merge(
    df_group, df_hour, how='left', on=[
        '日期', '网元', '网元名称', '小区', '小区名称', '下行流量_MB'])
df_busy_hour.sort_values(['下行平均激活用户数'], axis=0, ascending=False, inplace=True)
df_busy_hour.drop_duplicates(['日期', '小区名称'], keep='first', inplace=True)


df_busy_hour.sort_values(['下行流量_MB'], axis=0, ascending=False, inplace=True)
df_busy_typical = df_busy_hour.groupby(['网元', '网元名称', '小区', '小区名称'], as_index=False).head(10)
df_busy_typical['下行流量_MB'] = df_busy_typical['下行流量_MB'].map(lambda x:float(x.replace(',','')))
df_busy_typical['下行PRB平均占用率'] = df_busy_typical['下行PRB平均占用率'].map(lambda x:float(x.replace('%','')))
df_cell_typical = df_busy_typical.groupby(['网元', '网元名称', '小区', '小区名称'],as_index=False)[['下行流量_MB','最大RRC连接用户数','平均RRC连接用户数','平均激活用户数','下行PRB平均占用率','下行体验流量_MB']].agg(np.mean)
df_bts_typical = df_cell_typical.groupby(['网元', '网元名称'],as_index=False)[['下行流量_MB','最大RRC连接用户数','平均RRC连接用户数','平均激活用户数','下行PRB平均占用率','下行体验流量_MB']].agg({'下行流量_MB':np.sum, '最大RRC连接用户数':np.sum, '平均RRC连接用户数':np.sum, '平均激活用户数':np.sum, '下行PRB平均占用率':np.max, '下行体验流量_MB':np.min})

df_cell_typical.sort_values(['下行流量_MB'], axis=0, ascending=False, inplace=True)
df_bts_typical.sort_values(['下行流量_MB'], axis=0, ascending=False, inplace=True)
df_cell_typical['下行流量_MB'] = df_cell_typical['下行流量_MB'].map(lambda x:round(x/1024,2))
df_bts_typical['下行流量_MB'] = df_bts_typical['下行流量_MB'].map(lambda x:round(x/1024,2))

with pd.ExcelWriter('./2月24日-3月24日典型值.xlsx') as writer:
    df_bts_typical.to_excel(writer, '基站详单',index = False)
    df_cell_typical.to_excel(writer, '小区详单',index = False)

