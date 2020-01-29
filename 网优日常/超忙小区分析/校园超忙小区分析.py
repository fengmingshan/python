# -*- coding: utf-8 -*-
# @Author: fengmingshan
# @Date:   2019-09-02 15:15:02
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-06 17:12:31

import pandas as pd
import numpy as np
import os
import math

data_path = 'd:/2019年工作/2019年9月校园超忙小区分析/'
file = '能源学校_曲靖KPI指标_08-29_09.02.csv'
df_content = pd.read_csv(data_path + file, engine='python', skiprows=5)

df_content = df_content[['开始时间',
                         '结束时间',
                         '网元',
                         '网元名称',
                         '小区',
                         '小区名称',
                         '空口上行用户面流量（MByte）_1',
                         '空口下行用户面流量（MByte）_1477070755617-11',
                         '分QCI用户体验下行平均速率（Mbps）_1',
                         '下行PRB平均占用率_1',
                         'PDCCH信道CCE占用率_1',
                         '最大RRC连接用户数_1',
                         '平均RRC连接用户数_1',
                         '下行平均激活用户数_1',
                         '最大激活用户数_1',
                         'CQI优良比(>=7比例)']]
df_content['平均RRC连接用户数_1'] = df_content['平均RRC连接用户数_1'].map(
    lambda x: math.ceil(x))
df_content['下行平均激活用户数_1'] = df_content['下行平均激活用户数_1'].map(
    lambda x: math.ceil(x))
df_content['空口下行用户面流量（MByte）_1477070755617-11'] = df_content['空口下行用户面流量（MByte）_1477070755617-11'].map(
    lambda x: float(x.replace(',', '')) / 1024)
df_content['空口上行用户面流量（MByte）_1'] = df_content['空口上行用户面流量（MByte）_1'].map(
    lambda x: float(x.replace(',', '')) / 1024)

df_content['分QCI用户体验下行平均速率（Mbps）_1'] = round(
    df_content['分QCI用户体验下行平均速率（Mbps）_1'] / 8, 1)
df_content['总流量(GB)'] = df_content['空口上行用户面流量（MByte）_1'] + \
    df_content['空口下行用户面流量（MByte）_1477070755617-11']

df_content.rename(columns={'空口上行用户面流量（MByte）_1': '上行流量（GB）',
                           '空口下行用户面流量（MByte）_1477070755617-11': '下行流量（GB）',
                           '分QCI用户体验下行平均速率（Mbps）_1': '用户体验速率（MBps）',
                           }, inplace=True)
df_content['单用户平均流量（MByte）'] = df_content['下行流量（GB）'] / \
    df_content['下行平均激活用户数_1']

df_content['日期'] = df_content['开始时间'].apply(lambda x: x.split(' ')[0])
df_content['小时'] = df_content['开始时间'].apply(
    lambda x: x.split(' ')[1].split(':')[0])

df_content['下行PRB平均占用率_1'] =

# =============================================================================
# 总体情况按小时分析
# =============================================================================
df_all = pd.pivot_table(
    df_content,
    index=[
        '网元',
        '网元名称',
        '小区',
        '小区名称',
        '日期',
        '小时'],
    values=[
        '最大RRC连接用户数_1',
        '平均RRC连接用户数_1',
        '下行平均激活用户数_1',
        '最大激活用户数_1',
        '总流量(GB)',
        '下行PRB平均占用率_1'],

    aggfunc={
        '最大RRC连接用户数_1': np.sum,
        '平均RRC连接用户数_1': np.sum,
        '下行平均激活用户数_1': np.sum,
        '最大激活用户数_1': np.sum,
        '总流量(GB)': np.sum,
        '下行PRB平均占用率_1': np.mean})



# =============================================================================
# 用户数TOP
# =============================================================================
df_max_users = pd.pivot_table(
    df_content,
    index=[
        '网元',
        '网元名称',
        '小区',
        '小区名称'],
    values=[
        '最大RRC连接用户数_1',
        '平均RRC连接用户数_1',
        '下行平均激活用户数_1',
        '最大激活用户数_1'],
    aggfunc={
        '最大RRC连接用户数_1': np.max,
        '平均RRC连接用户数_1': np.max,
        '下行平均激活用户数_1': np.max,
        '最大激活用户数_1': np.max})
df_max_users.reset_index(inplace=True)
df_max_users.sort_values(by=['最大激活用户数_1'], ascending=False, inplace=True)
df_max_users = df_max_users[['网元',
                             '网元名称',
                             '小区',
                             '小区名称',
                             '最大激活用户数_1',
                             '下行平均激活用户数_1',
                             '最大RRC连接用户数_1',
                             '平均RRC连接用户数_1']]

# =============================================================================
# 流量TOP
# =============================================================================
df_max_throughput = pd.pivot_table(
    df_content,
    index=['网元',
           '网元名称',
           '小区',
           '小区名称'],
    values=['下行流量（MByte）'],
    aggfunc={
        '下行流量（GB）': np.max})
df_max_throughput.reset_index(inplace=True)
df_max_throughput.sort_values(
    by=['下行流量（GB）'],
    ascending=False,
    inplace=True)

# =============================================================================
# 速率TOP
# =============================================================================
df_min_speed = pd.pivot_table(
    df_content,
    index=['网元',
           '网元名称',
           '小区',
           '小区名称'],
    values=['用户体验速率（MBps）'],
    aggfunc={
        '用户体验速率（MBps）': np.min})
df_max_speed.reset_index(inplace=True)
df_max_speed.sort_values(
    by=['用户体验速率（MBps）'],
    ascending=True,
    inplace=True)
