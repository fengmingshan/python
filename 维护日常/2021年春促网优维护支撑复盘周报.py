# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:18:02 2021

@author: Administrator
"""

import pandas as pd
import os
import numpy as np

import seaborn as sns
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
myfont=FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf',size=36)
sns.set(font=myfont.get_name())
sns.despine(top = True,bottom=True, left =True, right= True)
sns.set_context("talk", font_scale=1.1)

path = r'C:\Users\Administrator\Desktop\各县清单'
os.chdir(path)

files = [x for x in os.listdir(path) if '按支局详单.xlsx' in x]

file_list = []
for file in files:
    df_tmp = pd.read_excel(file,sheet_name = '两周数据对比')
    df_tmp  = df_tmp[df_tmp['区县'] != '全县']
    file_list.append(df_tmp)

df_all = pd.concat(file_list, axis = 0)

df_all.columns
df_all['区县支局'] = df_all['区县'] + df_all['支局']

# 绘制用户数TOP分析图表
df_rrc_user = df_all[[
        '区县支局',
        '忙时RRC最大连接用户数_上周',
        '忙时RRC最大连接用户数_本周'
]]
df_rrc_user['数量增长top'] = df_rrc_user['忙时RRC最大连接用户数_本周'] - df_rrc_user['忙时RRC最大连接用户数_上周']
df_rrc_user['增长率top'] = (df_rrc_user['忙时RRC最大连接用户数_本周'] - df_rrc_user['忙时RRC最大连接用户数_上周'])/df_rrc_user['忙时RRC最大连接用户数_上周']

df_rrc_user_num_top = df_rrc_user.sort_values(by = '数量增长top', ascending = False)
df_rrc_user_rate_top = df_rrc_user.sort_values(by = '增长率top', ascending = False)

df_rrc_user_num_top = df_rrc_user_num_top.head(10)
plt.figure(figsize=(14, 8))
ax = sns.barplot(
        x="区县支局",
        y="数量增长top",
        data=df_rrc_user_num_top
)
for x, y in enumerate(df_rrc_user_num_top['数量增长top'].values):
    plt.text(x, y+50, "%s" %y)
ax.set_title('用户增长数量TOP10')
sns.despine(top = True,bottom=True, left =True, right= True)
pic = ax.get_figure()
pic.savefig('数量增长top', dpi = 80, bbox_inches = 'tight')

df_rrc_user_rate_top.columns
df_rrc_user_rate_top = df_rrc_user_rate_top.head(10)
plt.figure(figsize=(14, 8))
ax = sns.barplot(
        x="区县支局",
        y="增长率top",
        data=df_rrc_user_rate_top,
)
for x, y in enumerate(df_rrc_user_rate_top['增长率top'].values):
    plt.text(x, y+0.05, "%s" %round(y,1))
ax.set_title('用户增长率TOP10(%)')
sns.despine(top = True,bottom=True, left =True, right= True)
pic = ax.get_figure()
pic.savefig('用户增长率top', dpi = 80, bbox_inches = 'tight')

# 绘制流量TOP分析图表
df_throughput = df_all[[
        '区县支局',
        '总流量(GB)_上周',
        '总流量(GB)_本周'
]]
df_throughput['流量增长top'] = df_throughput['总流量(GB)_本周'] - df_throughput['总流量(GB)_上周']
df_throughput['流量增长率top'] = (df_throughput['总流量(GB)_本周'] - df_throughput['总流量(GB)_上周'])/df_throughput['总流量(GB)_上周']

df_throughput_top = df_throughput.sort_values(by = '流量增长top', ascending = False)
df_throughput_rate_top = df_throughput.sort_values(by = '流量增长率top', ascending = False)

df_throughput_top = df_throughput_top.head(10)
plt.figure(figsize=(14, 8))
ax = sns.barplot(
        x="区县支局",
        y="流量增长top",
        data=df_throughput_top
)
for x, y in enumerate(df_throughput_top['流量增长top'].values):
    plt.text(x-0.3, y+50, "%s" %round(y,1))
ax.set_title('流量增长TOP10(GB)')
sns.despine(top = True,bottom=True, left =True, right= True)
pic = ax.get_figure()
pic.savefig('流量增长TOP10', dpi = 80, bbox_inches = 'tight')

df_throughput_rate_top = df_throughput_rate_top.head(10)
plt.figure(figsize=(14, 8))
ax = sns.barplot(
        x="区县支局",
        y="流量增长率top",
        data=df_throughput_rate_top
)
for x, y in enumerate(df_throughput_rate_top['流量增长率top'].values):
    plt.text(x-0.2, y+0.01, "%s" %round(y,1))
ax.set_title('流量增长率top(%)')
sns.despine(top = True,bottom=True, left =True, right= True)
pic = ax.get_figure()
pic.savefig('流量增长率top', dpi = 80, bbox_inches = 'tight')

# 绘制PRB利用率TOP分析图表
df_prb = df_all[[
        '区县支局',
        '下行PRB利用率_本周'
]]
df_prb = df_prb.sort_values(by = '下行PRB利用率_本周', ascending = False)
df_prb = df_prb.head(10)

plt.figure(figsize=(14, 8))
ax = sns.barplot(
        x="区县支局",
        y="下行PRB利用率_本周",
        data=df_prb
)
for x, y in enumerate(df_prb['下行PRB利用率_本周'].values):
    plt.text(x-0.2, y+0.05, "%s" %round(y,1))
ax.set_title('PRB利用率TOP10(%)')
sns.despine(top = True,bottom=True, left =True, right= True)
pic = ax.get_figure()
pic.savefig('PRB利用率', dpi = 80, bbox_inches = 'tight')

# 绘制用户体验速率TOP分析图表
df_rate = df_all[[
        '区县支局',
        '用户体验速率_本周'
]]
df_rate = df_rate.sort_values(by = '用户体验速率_本周', ascending = True)
df_rate = df_rate.head(10)
plt.figure(figsize=(14, 8))
ax = sns.barplot(
        x="区县支局",
        y="用户体验速率_本周",
        data=df_rate
)
for x, y in enumerate(df_rate['用户体验速率_本周'].values):
    plt.text(x-0.2, y+0.2, "%s" %round(y,1))
ax.set_title('用户体验速率(Mbps)')
sns.despine(top = True,bottom=True, left =True, right= True)
pic = ax.get_figure()
pic.savefig('用户体验速率', dpi = 80, bbox_inches = 'tight')

with pd.ExcelWriter('增长情况.xlsx') as f:
    df_throughput_top.to_excel(f, sheet_name = '用户增长量', index = False)
    df_rrc_user_rate_top.to_excel(f, sheet_name = '用户增长率', index = False)
    df_throughput_top.to_excel(f, sheet_name = '流量增长', index = False)
    df_throughput_rate_top.to_excel(f, sheet_name = '流量增长率', index = False)
    df_prb.to_excel(f, sheet_name = 'PRB利用率', index = False)
    df_rate.to_excel(f, sheet_name = '用户体验速率', index = False)
