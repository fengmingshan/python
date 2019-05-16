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

KPI_date = df_city.loc[0,'开始时间'].split(' ')[0]
                
# =============================================================================
# 全市昨日VOLTE指标分析
# =============================================================================
def draw_KPI(df,text):
    '''画VOLTE关键指标图'''
    df['hour'] = df['开始时间'].map(lambda x:x[11:13])
    # 画VOLTE户数
    y1 = df['[LTE]下行QCI1最大激活用户数'].T.values
    y2 = df['[LTE]下行QCI2最大激活用户数'].T.values
    x1 = df['hour'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='VOLTE语音用户数',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=4) 
    plt.plot(range(len(x1)),y2,label='VOLTE视频用户数',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=4) 
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
    for a,b in zip(range(len(x1)),y2):
        plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('小时')
    plt.ylabel(text + '_VOLTE用户数')
    plt.title(text + '_VOLTE用户数')
    plt.legend(loc='center right')
    plt.savefig(pic_path + text + "VOLTE用户数.png",format='png', dpi=400)  
    plt.close
    
    # 画VOLTE呼叫次数
    y1 = df['[LTE]E-RAB建立请求数目(QCI=1)'].T.values
    y2 = df['[LTE]E-RAB建立请求数目(QCI=2)'].T.values
    df['hour'] = df['开始时间'].map(lambda x:x[11:13])
    x1 = df['hour'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='VOLTE语音用户数',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=4) 
    plt.plot(range(len(x1)),y2,label='VOLTE视频用户数',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=4) 
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
    for a,b in zip(range(len(x1)),y2):
        plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('小时')
    plt.ylabel(text + '_VOLTE呼叫数')
    plt.title(text + '_VOLTE呼叫数')
    plt.legend(loc='center right')
    plt.savefig(pic_path + text +  "VOLTE呼叫次数.png",format='png', dpi=400)  
    plt.close
    
    
    # 画VOLTE掉话率
    df['[FDD]E-RAB掉话率(QCI=1)'] = df['[FDD]E-RAB掉话率(QCI=1)'].str.strip("%").astype(float)
    df['[FDD]E-RAB掉话率(QCI=2)'] = df['[FDD]E-RAB掉话率(QCI=2)'].str.strip("%").astype(float)
    y1 = df['[FDD]E-RAB掉话率(QCI=1)'].T.values
    y2 = df['[FDD]E-RAB掉话率(QCI=2)'].T.values
    df['hour'] = df['开始时间'].map(lambda x:x[11:13])
    x1 = df['hour'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='VOLTE语音掉话率',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=4) 
    plt.plot(range(len(x1)),y2,label='VOLTE视频掉话率',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=4) 
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.001, '%.2f%%' % b, ha='center', va= 'bottom',fontsize=8)
    for a,b in zip(range(len(x1)),y2):
        plt.text(a,b*1.001, '%.2f%%'% b, ha='center', va= 'bottom',fontsize=8)
    plt.xlabel('小时')
    plt.ylabel(text + '_VOLTE掉话率')
    plt.title(text + '_VOLTE掉话率')
    plt.legend(loc='center right')
    plt.savefig(pic_path + text + "VOLTE掉话率.png",format='png', dpi=400)  
    plt.close
    
    # 画VOLTE语音接通率
    df['[LTE]小区业务相关的无线接通率(QCI=1)'] = df['[LTE]小区业务相关的无线接通率(QCI=1)'].str.strip("%").astype(float)
    y1 = df['[LTE]小区业务相关的无线接通率(QCI=1)'].T.values
    df['hour'] = df['开始时间'].map(lambda x:x[11:13])
    x1 = df['hour'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='VOLTE语音接通率',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=5) 
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.0001,'%.2f%%' % b, ha='center', va= 'bottom',fontsize=8)
    plt.xlabel('小时')
    plt.ylabel(text + '_VOLTE语音接通率')
    plt.title(text + '_VOLTE语音接通率')
    plt.legend(loc='center right')
    plt.savefig(pic_path + text + "VOLTE语音接通率.png",format='png', dpi=400)  
    plt.close
    
    # 画VOLTE视频接通率
    df['[LTE]小区业务相关的无线接通率(QCI=2)'] = df['[LTE]小区业务相关的无线接通率(QCI=2)'].str.strip("%").astype(float)
    y2 = df['[LTE]小区业务相关的无线接通率(QCI=2)'].T.values
    df['hour'] = df['开始时间'].map(lambda x:x[11:13])
    x1 = df['hour'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y2,label='VOLTE视频接通率',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=5) 
    for a,b in zip(range(len(x1)),y2):
        plt.text(a,b*1.0001, '%.2f%%' % b, ha='center', va= 'bottom',fontsize=8)
    plt.xlabel('小时')
    plt.ylabel(text + '_VOLTE视频接通率')
    plt.title(text + '_VOLTE视频接通率')
    plt.legend(loc='center right')
    plt.savefig(pic_path + text + "VOLTE视频接通率.png",format='png', dpi=400)  
    plt.close

draw_KPI(df_city,'全市')

# =============================================================================
# L800_VOLTE指标分析
# =============================================================================
df_subnet['子网名称'] = df_subnet['子网名称'].map(lambda x:x.replace('曲靖','').split('(')[0].split(' ')[0])
subnet_name = sorted(list(set(df_subnet['子网名称'])))
for name in subnet_name:
    df_country =  df_subnet[df_subnet['子网名称'] == name]
    draw_KPI(df_country,name)

# =============================================================================
# TOP小区分析
# =============================================================================
df_cell['hour'] = df_cell['开始时间'].map(lambda x:x[11:13])
df_cell['[LTE]E-RAB建立请求数目(QCI=1)'] = df_cell['[LTE]E-RAB建立请求数目(QCI=1)'].astype(int)
df_cell['[LTE]小区业务相关的无线接通率(QCI=1)'] = df_cell['[LTE]小区业务相关的无线接通率(QCI=1)'].str.strip("%").astype(float)
df_cell['RRC连接建立成功率_1498720732851-0-29'] = df_cell['RRC连接建立成功率_1498720732851-0-29'].str.strip("%").astype(float)
df_cell['[FDD]E-RAB掉话率(QCI=1)'] = df_cell['[FDD]E-RAB掉话率(QCI=1)'].str.strip("%").astype(float)

df_connect_top = df_cell[(df_cell['[LTE]E-RAB建立请求数目(QCI=1)'] > 3 ) & (df_cell['[LTE]小区业务相关的无线接通率(QCI=1)'] <= 0.98)]
df_connect_top = df_connect_top[['网元','小区','小区名称','[LTE]小区业务相关的无线接通率(QCI=1)','[LTE]E-RAB建立请求数目(QCI=1)','RRC连接建立成功率_1498720732851-0-29']]
df_connect_top = df_connect_top.sort_values(by=['[LTE]E-RAB建立请求数目(QCI=1)','[LTE]小区业务相关的无线接通率(QCI=1)'],ascending = [False,True]) # 按时间顺序升序排列  

df_drop_top = df_cell[(df_cell['[FDD]E-RAB掉话率(QCI=1)'] > 0.002 ) & (df_cell['[LTE]E-RAB建立请求数目(QCI=1)'] > 3)]
df_drop_top = df_drop_top[['网元','小区','小区名称','[FDD]E-RAB掉话率(QCI=1)','[LTE]E-RAB建立请求数目(QCI=1)']]
df_drop_top = df_drop_top.sort_values(by=['[LTE]E-RAB建立请求数目(QCI=1)','[FDD]E-RAB掉话率(QCI=1)'],ascending = [False,False]) # 按时间顺序升序排列  


# =============================================================================
# 输出报表
# =============================================================================
with  pd.ExcelWriter(report_path + 'VOLTE_指标分析(日)_' + KPI_date + '.xlsx')  as writer:  #输出到excel
    book = writer.book 
    sheet = book.add_worksheet('全市')
    sheet.insert_image('A2' , pic_path + "全市VOLTE语音接通率.png")
    sheet.insert_image('A23', pic_path + "全市VOLTE掉话率.png")
    sheet.insert_image('A44', pic_path + "全市VOLTE呼叫次数.png")
    sheet.insert_image('A65', pic_path + "全市VOLTE用户数.png")
    sheet.insert_image('A86', pic_path + "全市VOLTE视频接通率.png")
    for name in subnet_name:
        sheet = book.add_worksheet(name)
        sheet.insert_image('A2' , pic_path + name + "VOLTE语音接通率.png")
        sheet.insert_image('A23', pic_path + name + "VOLTE掉话率.png")
        sheet.insert_image('A44', pic_path + name + "VOLTE呼叫次数.png")
        sheet.insert_image('A65', pic_path + name + "VOLTE用户数.png")
        sheet.insert_image('A86', pic_path + name + "VOLTE视频接通率.png")

with  pd.ExcelWriter(report_path + 'VOLTE_TOP小区分析(日)_' + KPI_date + '.xlsx')  as writer:  #输出到excel
    df_connect_top.to_excel(writer,'呼叫成功率',index = False)
    df_drop_top.to_excel(writer,'掉话率',index = False)

    




