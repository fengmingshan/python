#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
from datetime import datetime
from dateutil.parser import parse
from dateutil.rrule import *
from interval import Interval, IntervalSet

data_path = r'D:\_小程序\小区退服计算'
if not os.path.exists(data_path):
    os.mkdir(data_path)
if not os.path.exists(data_path + './报表输出'):
    os.mkdir(data_path + './报表输出')
os.chdir(data_path)

block_cell = '屏蔽小区.xlsx'

# 需要使用到的自定义函数


def 填写退服小区(a, b):
    if pd.isnull(a):
        return b.split('_')[0] + '_' + b.split('_')[1]
    else:
        return a

def calc_break_time(interval):
    low = interval.lower_bound
    upper = interval.upper_bound


df_block = pd.read_excel(block_cell)
df_block['退服小区标识'] = df_block.apply(
    lambda x: 填写退服小区(x.关联小区标识, x.告警对象名称), axis=1)
df_block['告警清除时间'] = df_block['告警清除时间'].map(str)
df_block.head(5)

df_block = df_block[['退服小区标识', '告警发生时间', '告警清除时间', '退服时长(分钟)', '6-8点退服时长（分钟）', '8-22点退服时长（分钟）',
                     '22-24点退服时长（分钟）']]

for i in range(len(df_block)):
    t0 = df_block.loc[i, '告警发生时间']
    t1 = df_block.loc[i, '告警清除时间']
    date_list = list(rrule(DAILY, dtstart=parse(t0), until=parse(t1)))
    day_list = [x.strftime('%Y-%m-%d') for x in date_list]

    start_time = datetime.strptime(df_block.loc[0, '告警发生时间'], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(df_block.loc[0, '告警清除时间'], '%Y-%m-%d %H:%M:%S')

    # 创建
    break_interval = IntervalSet.between(start_time, end_time, closed=True)
    for day in day_list:
        # 创建三个时间段，分别是6-8点，8-22点，22-24点，
        interval_6to8 = IntervalSet.between(
            datetime.strptime(
                day + ' ' + '06:00:00',
                '%Y-%m-%d %H:%M:%S'),
            datetime.strptime(
                day + ' ' + '08:00:00',
                '%Y-%m-%d %H:%M:%S'), closed=True)
        interval_8to22 = IntervalSet.between(
            datetime.strptime(
                day + ' ' + '08:00:00',
                '%Y-%m-%d %H:%M:%S'),
            datetime.strptime(
                day + ' ' + '22:00:00',
                '%Y-%m-%d %H:%M:%S'), closed=True)
        interval_22to24 = IntervalSet.between(
            datetime.strptime(
                day + ' ' + '22:00:00',
                '%Y-%m-%d %H:%M:%S'),
            datetime.strptime(
                day + ' ' + '23:59:59',
                '%Y-%m-%d %H:%M:%S'), closed=True)

        break_6to8 = break_interval & intervla_6to8
        break_8to22 = break_interval & intervla_8to22
        break_22to24 = break_interval & intervla_22to24
        low = break_6to8.lower_bound()
        upper = break_6to8.upper_bound()
        break_time = upper - low


