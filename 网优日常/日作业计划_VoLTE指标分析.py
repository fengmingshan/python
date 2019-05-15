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

# 画VOLTE户数
y1 = df_city['[LTE]下行QCI1最大激活用户数'].T.values
y2 = df_city['[LTE]下行QCI2最大激活用户数'].T.values
df_city['hour'] = df_city['开始时间'].map(lambda x:x[11:13])
x1 = df_city['hour'].T.values
plt.figure(figsize=(12, 4))
plt.xticks(range(len(x1)), x1,fontsize=8)
plt.plot(range(len(x1)),y1,label='VOLTE语音用户数',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=4) 
plt.plot(range(len(x1)),y2,label='VOLTE视频用户数',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=4) 
for a,b in zip(range(len(x1)),y1):
    plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
for a,b in zip(range(len(x1)),y2):
    plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('时间')
plt.ylabel('全市VOLTE用户数')
plt.title('全市VOLTE用户数')
plt.legend(loc='center right')
plt.savefig(pic_path + "全市VOLTE用户数.png",format='png', dpi=400)  
plt.close

# 画VOLTE呼叫次数
y1 = df_city['[LTE]E-RAB建立请求数目(QCI=1)'].T.values
y2 = df_city['[LTE]E-RAB建立请求数目(QCI=2)'].T.values
df_city['hour'] = df_city['开始时间'].map(lambda x:x[11:13])
x1 = df_city['hour'].T.values
plt.figure(figsize=(12, 4))
plt.xticks(range(len(x1)), x1,fontsize=8)
plt.plot(range(len(x1)),y1,label='VOLTE语音用户数',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=4) 
plt.plot(range(len(x1)),y2,label='VOLTE视频用户数',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=4) 
for a,b in zip(range(len(x1)),y1):
    plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
for a,b in zip(range(len(x1)),y2):
    plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('时间')
plt.ylabel('全市VOLTE用户数')
plt.title('全市VOLTE用户数')
plt.legend(loc='center right')
plt.savefig(pic_path + "全市VOLTE呼叫次数.png",format='png', dpi=400)  
plt.close


# 画VOLTE掉话率
df_city['[FDD]E-RAB掉话率(QCI=1)'] = df_city['[FDD]E-RAB掉话率(QCI=1)'].map(lambda x:x[0:-1]).astype(float)
df_city['[FDD]E-RAB掉话率(QCI=2)'] = df_city['[FDD]E-RAB掉话率(QCI=2)'].map(lambda x:x[0:-1]).astype(float)
y1 = df_city['[FDD]E-RAB掉话率(QCI=1)'].T.values
y2 = df_city['[FDD]E-RAB掉话率(QCI=2)'].T.values
df_city['hour'] = df_city['开始时间'].map(lambda x:x[11:13])
x1 = df_city['hour'].T.values
plt.figure(figsize=(12, 4))
plt.xticks(range(len(x1)), x1,fontsize=8)
plt.plot(range(len(x1)),y1,label='VOLTE语音掉话率',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=4) 
plt.plot(range(len(x1)),y2,label='VOLTE视频掉话率',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=4) 
for a,b in zip(range(len(x1)),y1):
    plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
for a,b in zip(range(len(x1)),y2):
    plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
plt.xlabel('时间')
plt.ylabel('全市VOLTE掉话率')
plt.title('全市VOLTE掉话率')
plt.legend(loc='center right')
plt.savefig(pic_path + "全市VOLTE掉话率.png",format='png', dpi=400)  
plt.close

# 画VOLTE语音接通率
df_city['[LTE]小区业务相关的无线接通率(QCI=1)'] = df_city['[LTE]小区业务相关的无线接通率(QCI=1)'].map(lambda x:x[0:-1]).astype(float)
y1 = df_city['[LTE]小区业务相关的无线接通率(QCI=1)'].T.values
df_city['hour'] = df_city['开始时间'].map(lambda x:x[11:13])
x1 = df_city['hour'].T.values
plt.figure(figsize=(12, 4))
plt.xticks(range(len(x1)), x1,fontsize=8)
plt.plot(range(len(x1)),y1,label='VOLTE语音接通率',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=5) 
for a,b in zip(range(len(x1)),y1):
    plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=10)
plt.xlabel('时间')
plt.ylabel('全市VOLTE掉话率')
plt.title('全市VOLTE掉话率')
plt.legend(loc='center right')
plt.savefig(pic_path + "全市VOLTE语音接通率.png",format='png', dpi=400)  
plt.close

# 画VOLTE视频接通率
df_city['[LTE]小区业务相关的无线接通率(QCI=2)'] = df_city['[LTE]小区业务相关的无线接通率(QCI=2)'].map(lambda x:x[0:-1]).astype(float)
y2 = df_city['[LTE]小区业务相关的无线接通率(QCI=2)'].T.values
df_city['hour'] = df_city['开始时间'].map(lambda x:x[11:13])
x1 = df_city['hour'].T.values
plt.figure(figsize=(12, 4))
plt.xticks(range(len(x1)), x1,fontsize=8)
plt.plot(range(len(x1)),y2,label='VOLTE视频接通率',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=5) 
for a,b in zip(range(len(x1)),y2):
    plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=10)
plt.xlabel('时间')
plt.ylabel('全市VOLTE掉话率')
plt.title('全市VOLTE掉话率')
plt.legend(loc='center right')
plt.savefig(pic_path + "全市VOLTE视频接通率.png",format='png', dpi=400)  
plt.close

with  pd.ExcelWriter(report_path + 'VOLTE指标分析(日)_' + current_date + '.xlsx')  as writer:  #输出到excel
    book = writer.book 
    sheet = book.add_worksheet('全市')
    sheet.insert_image('A2' , pic_path + "全市VOLTE用户数.png")
    sheet.insert_image('A23', pic_path + "全市VOLTE呼叫次数.png")
    sheet.insert_image('A44', pic_path + "全市VOLTE掉话率.png")
    sheet.insert_image('A65', pic_path + "全市VOLTE语音接通率.png")
    sheet.insert_image('A86', pic_path + "全市VOLTE视频接通率.png")

    




