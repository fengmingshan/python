# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 16:23:08 2019

@author: Administrator
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

path ='D:/_小程序/感知工单分析报告'
pic_path = 'D:/_小程序/感知工单分析报告/pic'
if not os.path.exists(pic_path):
    os.mkdir(pic_path)

file = '历史性能_曲靖KPI指标_20190930164320.csv'
os.chdir(path)

df = pd.read_csv(file,skiprows = 5,engine ='python')
df['hour'] = df['开始时间'].map(lambda x:x.split(' ')[1][:2])
hour_list = list(set(df['hour']))
for hour in hour_list:
    df_tmp = df[df['hour'] == hour]
    ind = df.groupby(by='hour', as_index=True)['最大RRC连接用户数_1'].agg(sum).argmax()
df_busy = df[df['hour'] == ind]

df_busy['下行PRB平均占用率_1'] = df_busy['下行PRB平均占用率_1'].map(lambda x:float(x.replace('%','')))
df_busy['E-RAB掉线率_1'] = df_busy['E-RAB掉线率_1'].map(lambda x:float(x.replace('%','')))
df_busy['time'] = df_busy['开始时间'].map(lambda x:x[5:])

def draw_line_chart(df,time_col,data_col):
    x1 = df[time_col].values
    y1 = df[data_col].values
    plt.figure(figsize=(14, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label=data_col,linewidth=3,color='b',marker='o',markerfacecolor='yellow',markersize=6)
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.001 , b , ha='center', va= 'bottom', fontsize=10)
    plt.xlabel('时间')
    plt.ylabel(data_col)
    plt.title(data_col)
    plt.legend(bbox_to_anchor=(1.05, 0.5), loc='upper left', borderaxespad=0.)
    plt.savefig(pic_path + data_col + '.png',format='png', dpi=400)
    plt.show('hold')

def draw_bar_chart(df,time_col,data_col):
    x2= df[time_col].values
    y2 = df[data_col].values
    plt.figure(figsize=(14, 4))
    plt.bar(x2,y2,color='g',width = 0.3,alpha=0.6,label=data_col)
    for x,y in zip(x2,y2):
        plt.text(x, y*1.005, y, ha='center', va= 'bottom',fontsize=8)
    plt.xlabel('时间')
    plt.xticks(range(0,len(x2)),x2)
    plt.ylabel(data_col)
    # 将图例扩展到图片外部，x坐标1.05在图片外部0.05处，y坐标在图片中间，borderaxespad=0.表示扩展到图片外部
    plt.legend(bbox_to_anchor=(1.05, 0.5), loc='upper left', borderaxespad=0.)
    plt.title(data_col)
    plt.savefig(pic_path + data_col + ".png",format='png', dpi=200)
    plt.show('hold')

draw_line_chart(df_busy,'time','下行PRB平均占用率_1')
draw_line_chart(df_busy,'time','E-RAB掉线率_1')



draw_bar_chart(df_busy,'time','最大RRC连接用户数_1')
draw_bar_chart(df_busy,'time','下行平均激活用户数_1')
draw_bar_chart(df_busy,'time','最大激活用户数_1')
draw_bar_chart(df_busy,'time','Total DL Data Volume(GB)')


