# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:24:12 2019

@author: Administrator
"""
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd 
import os
import numpy as np
from datetime import datetime 
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from pyecharts.charts  import Line
from pyecharts.charts  import Bar
from snapshot_selenium import snapshot

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

#设置工作目录
current_date = str(datetime.now()).split('.')[0].split(' ')[0]
data_path = r'D:\_VoLTE网络健康检查（日）' + '\\'

# =============================================================================
# 采集原始数据文件及创建所需工作目录
# =============================================================================
all_files = os.listdir(data_path)
files = [x for x in all_files if '.csv' in x ]

if '报表输出' not in all_files:
    os.makedirs(data_path + '报表输出' + '\\' )
report_path = data_path + '报表输出' + '\\'

if 'PIC' not in all_files:
    os.makedirs(data_path + 'PIC' + '\\' )
pic_path = data_path + 'PIC' + '\\' 

df_cell = pd.DataFrame()
df_subnet = pd.DataFrame() 
df_city = pd.DataFrame() 
 
for file in files:
    with open(data_path + file) as tmpfile:
        line = tmpfile.readline()
        if '历史性能' in line:
            df_tmp = pd.read_csv(data_path + file,engine = 'python',skiprows = 5 )
            columns = list(df_tmp.columns)
            if '小区名称' in columns:
                df_cell = df_cell.append(df_tmp)
            elif '子网名称' in columns and '小区名称' not in columns:
                df_subnet = df_subnet.append(df_tmp)
            else :
                df_city = df_city.append(df_tmp)
        else:
            df_tmp = pd.read_csv(data_path + file,engine = 'python')
            columns = list(df_tmp.columns)
            if '小区名称' in columns:
                df_cell = df_cell.append(df_tmp)
            elif '子网名称' in columns and '小区名称' not in columns:
                df_subnet = df_subnet.append(df_tmp)
            else :
                df_city = df_city.append(df_tmp)
                
# =============================================================================
# 全市昨日VOLTE指标分析
# =============================================================================

# 画VOLTE用户数
y1 = df_city['[LTE]下行QCI1最大激活用户数'].T.values
df_city['hour'] = df_city['开始时间'].map(lambda x:x[11:13])
x1 = df_city['hour'].T.values
plt.figure(figsize=(12, 4))
plt.xticks(range(len(x1)), x1,fontsize=8)
plt.plot(range(len(x1)),y1,label='VOLTE语音用户数',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
for a,b in zip(range(len(x1)),y1):
    plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=9)
plt.xlabel('日期')
plt.ylabel('全市VOLTE语音用户数')
plt.title('全市VOLTE语音用户数')
plt.legend(loc='center right')
plt.savefig(pic_path + "全市VOLTE语音用户数.png",format='png', dpi=400)  
plt.show

