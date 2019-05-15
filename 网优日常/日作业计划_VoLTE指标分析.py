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

if 'PIC' not in all_files:
    os.makedirs(data_path + 'PIC' + '\\' )

df_cell = pd.DataFrame()
df_subnet = pd.DataFrame() 
df_city = pd.DataFrame() 
 
for file in files:
    df_tmp = pd.read_csv(data_path + file,engine = 'python',skiprows = 5 )
    columns = list(df_tmp.columns)
    if '小区名称' in columns:
        df_cell.append(df_tmp)
    elif '子网名称' in columns:
        df_subnet.append(df_tmp)
    else :
        df_city = df_data.append(df_tmp)

# =============================================================================
# 全市昨日VOLTE指标分析
# =============================================================================
df_city = pd.pivot_table(df_data, index=['开始时间'], 
                                  values =['CQI上报总次数' ,'CQI大于等于7次数'], 
                                  aggfunc = {'CQI上报总次数':np.sum,'CQI大于等于7次数':np.sum})     


