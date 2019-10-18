#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import time
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

def calc_time(interval):
    '''
    根据告警的interval计算出时长，单位：minutes
    '''
    if interval != IntervalSet.empty():
        low = interval.lower_bound()
        upper = interval.upper_bound()
        break_time = upper - low
        break_minutes = round(break_time.seconds/60,2)
    else:
        break_minutes = 0
    return break_minutes

def calc_break_time(bts_level,t0,t1):
    '''
    根据告警发生时间 t0 和 告警结束时间 t1
    计算出在三个考核时段内告警的时长，单位：minutes
    '''
#    t0 = df_block.loc[0,'告警发生时间']
#    t1 = df_block.loc[0,'告警清除时间']
    date_list = list(rrule(DAILY, dtstart=parse(t0), until=parse(t1)))
    day_list = [x.strftime('%Y-%m-%d') for x in date_list]
    # 创建断站的时间段
    start_time = datetime.strptime(t0, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
    break_interval = IntervalSet.between(start_time, end_time, closed=True)
    break_time_6to8 = 0
    break_time_8to22 = 0
    break_time_22to24 = 0
    for day in day_list:
        # 创建三个考核时间段，分别是6-8点，8-22点，22-24点，
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
        break_interval_6to8 = break_interval & interval_6to8
        break_interval_8to22 = break_interval & interval_8to22
        break_interval_22to24 = break_interval & interval_22to24

        break_time_6to8 += calc_time(break_interval_6to8)
        break_time_8to22 += calc_time(break_interval_8to22)
        break_time_22to24 += calc_time(break_interval_22to24)
    if bts_level == 'A' or  bts_level == 'B':
        return (break_time_6to8,break_time_8to22 * 1.2,break_time_22to24)
    else:
        return (break_time_6to8,break_time_8to22,break_time_22to24)

df_block = pd.read_excel(block_cell)
df_block['退服小区标识'] = df_block.apply(
    lambda x: 填写退服小区(x.关联小区标识, x.告警对象名称), axis=1)
df_block['告警发生时间'] = df_block['告警发生时间'].map(str)
df_block['告警清除时间'] = df_block['告警清除时间'].map(str)
df_block = df_block[['所属基站ID','退服小区标识','网元等级','告警发生时间', '告警清除时间', '退服时长(分钟)', '6-8点退服时长（分钟）', '8-22点退服时长（分钟）',
                     '22-24点退服时长（分钟）']]
df_block['alarm_time_index'] = df_block['退服小区标识'] + '_' + df_block['告警发生时间'].map(lambda x:x[:-6])

for i in range(len(df_block)):
    break_time = calc_break_time(df_block.loc[i,'网元等级'],df_block.loc[i,'告警发生时间'],df_block.loc[i,'告警清除时间'])
    df_block.loc[i,'6-8点退服时长（分钟）'] = break_time[0]
    df_block.loc[i,'8-22点退服时长（分钟）'] = break_time[1]
    df_block.loc[i,'22-24点退服时长（分钟）'] = break_time[2]

with  pd.ExcelWriter('./报表输出/'  + '被屏蔽小区真实时长.xlsx')  as writer:  #输出到excel
    df_block.to_excel(writer,'被屏蔽小区真实时长',index=False)


