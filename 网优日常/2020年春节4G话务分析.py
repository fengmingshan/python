# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 08:08:01 2020

@author: Administrator
"""

import pandas as pd
import os
import numpy
from datetime import datetime
from dateutil.parser import parse

work_path = 'D:/2020年工作/2020年2月春节4G话务分析/'
os.chdir(work_path)

titile = list(pd.read_excel('./原始数据/爱立信/title.xlsx').columns)
busy_titile = list(pd.read_excel('./原始数据/爱立信/busy_title.xlsx').columns)

df_eric = pd.read_csv('./原始数据/爱立信/爱立信0123-0319.csv', header=None, names=titile)
for col in ['DATE_ID', 'eNodeB', 'EUTRANCELLFDD']:
    df_eric[col] = df_eric[col].map(lambda x: x.replace('\'', ''))
df_eric = df_eric[['DATE_ID', 'eNodeB', 'EUTRANCELLFDD', 'Max number of UE in RRc',
                   'Air Interface_Traffic_Volume_UL_MBytes', 'Air Interface_Traffic_Volume_DL_MBytes']]
df_eric.rename(columns={'DATE_ID': '日期',
                        'EUTRANCELLFDD': '小区名称',
                        'Max number of UE in RRc': '最大RRC连接用户数',
                        'Air Interface_Traffic_Volume_UL_MBytes': '空口上行流量',
                        'Air Interface_Traffic_Volume_DL_MBytes': '空口下行流量'
                        }, inplace=True)
df_eric['总流量'] = df_eric['空口上行流量'] + df_eric['空口下行流量']
df_eric['日期'] = pd.to_datetime(df_eric['日期'])
df_eric['期间'] = ''
df_eric['期间'][(df_eric['日期'] >= parse('2020-01-23 00:00:00')) &
              (df_eric['日期'] < parse('2020-02-24 00:00:00'))] = '春节期间'
df_eric['期间'][(df_eric['日期'] >= parse('2020-02-24 00:00:00')) &
              (df_eric['日期'] < parse('2020-03-21 00:00:00'))] = '节后'

df_eric_busy = pd.read_csv('./原始数据/爱立信/爱立信0123-0319_busy.csv', header=None, names=busy_titile)
for col in ['DATE_ID', 'eNodeB', 'EUTRANCELLFDD']:
    df_eric_busy[col] = df_eric_busy[col].map(lambda x: x.replace('\'', ''))
df_eric_busy = df_eric_busy[['DATE_ID', 'eNodeB',
                             'EUTRANCELLFDD', 'Max number of UE in RRc', 'DL_Util_of_PRB']]
df_eric_busy.rename(columns={'DATE_ID': '日期',
                             'eNodeB': 'DO用户数',
                             'EUTRANCELLFDD': 'DO流量',
                             'Max number of UE in RRc': '最大RRC连接用户数',
                             'DL_Util_of_PRB': '下行PRB利用率',
                             }, inplace=True)
df_eric_busy['日期'] = pd.to_datetime(df_eric_busy['日期'])
df_eric_busy['期间'] = ''
df_eric_busy['期间'][(df_eric_busy['日期'] >= parse('2020-01-23')) &
                   (df_eric_busy['日期'] < parse('2020-02-24 00:00:00'))] = '春节期间'
df_eric_busy['期间'][(df_eric_busy['日期'] >= parse('2020-02-24')) &
                   (df_eric_busy['日期'] < parse('2020-03-21 00:00:00'))] = '节后'


df_zte = pd.read_csv(
    './原始数据/2020_03_19_11_51_59_279_qj_wxzx_zhouchaocheng_2439.csv', encoding='gbk')
df_tmp = df_zte.head(10)
