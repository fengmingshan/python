# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 09:09:46 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
import os
import xlsxwriter
import matplotlib.pyplot as plt
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

path_3g = r'D:\_话务周报(划小到支局)\3G' + '\\'
path_3g_busy = r'D:\_话务周报(划小到支局)\3G忙时' + '\\'

data_path = r'D:\_话务周报(划小到支局)' + '\\'
out_path = r'D:\_话务周报(划小到支局)\报表输出' + '\\'
pic_path = r'D:\_话务周报(划小到支局)\pic' + '\\'

files_3G = os.listdir(path_3g) 

df_zte_3G_traffic = pd.DataFrame()
for file in files_3G:    
    df_tmp = pd.read_csv(path_3g + file,engine = 'python', encoding = 'gbk')
    df_tmp.fillna(0,inplace=True)
    df_zte_3G_traffic = df_zte_3G_traffic.append(df_tmp)

    df_tmp['空口上行用户面流量（MByte）_1'] = df_tmp['空口上行用户面流量（MByte）_1'].map(lambda x:float(x.replace(',','')))
    df_tmp['空口下行用户面流量（MByte）_1477070755617-11'] = df_tmp['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:float(x.replace(',','')))
    df_tmp['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y-%m-%d")  
    week = str(df_tmp.iloc[0,1]).split(' ')[0][5:10] + "_" + str(df_tmp.iloc[-1,1]).split(' ')[0][5:10]
    df_tmp['week'] = week
    df_tmp.rename(columns={'空口上行用户面流量（MByte）_1':'上行流量(MB)',
                           '空口下行用户面流量（MByte）_1477070755617-11':'下行流量(MB)'},inplace =True)
    df_tmp['总流量(MB)'] =  df_tmp['上行流量(MB)'] + df_tmp['下行流量(MB)'] 
    df_tmp =  df_tmp[['week','网元','总流量(MB)']]
    df_pivot_traffic = pd.pivot_table(df_tmp, index=['week','网元'], 
                                              values = '总流量(MB)', 
                                              aggfunc = {'总流量(MB)':np.sum})  
    df_pivot_traffic = df_pivot_traffic.reset_index()                                                     
    df_zte_4G_traffic = df_zte_4G_traffic.append(df_pivot_traffic)
df_zte_4G_traffic['网元'] = df_zte_4G_traffic['网元'].astype(int)
df_zte_4G_traffic = pd.merge(df_zte_4G_traffic,df_zte_eNodeB,how ='left',on = '网元' )     


df_zte_4G_user = pd.DataFrame()
for file in zte_4G_busy_files:    
    df_tmp = pd.read_csv(path_4g_busy + file,skiprows = 5,engine = 'python', encoding = 'gbk')
    df_tmp.fillna(0,inplace=True)
    df_tmp['空口上行用户面流量（MByte）_1'] = df_tmp['空口上行用户面流量（MByte）_1'].map(lambda x:float(x.replace(',','')))
    df_tmp['空口下行用户面流量（MByte）_1477070755617-11'] = df_tmp['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:float(x.replace(',','')))
    df_tmp['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y-%m-%d")  
    # =============================================================================
    # 计算每日实际忙时确定RRC连接用户数
    # =============================================================================
    df_pivot_rrc = pd.pivot_table(df_tmp, index=['开始时间'], values = '最大RRC连接用户数_1', aggfunc = {'最大RRC连接用户数_1':np.sum})                                                  
    df_pivot_rrc = df_pivot_rrc.sort_values(by='最大RRC连接用户数_1',ascending = False)
    df_pivot_rrc = df_pivot_rrc.reset_index()
    busy_hour =  df_pivot_rrc.loc[0,'开始时间']
    df_max_rrc =  df_tmp[['开始时间','网元','最大RRC连接用户数_1']][df_tmp['开始时间'] == busy_hour]    
    week = str(df_tmp.iloc[0,1]).split(' ')[0][5:10] + "_" + str(df_tmp.iloc[-1,1]).split(' ')[0][5:10]
    df_max_rrc['week'] = week
    df_max_rrc.rename(columns={'最大RRC连接用户数_1':'RRC连接用户数'},inplace =True)
    df_max_rrc =  df_max_rrc[['week','网元','RRC连接用户数']]
    df_zte_4G_user = df_zte_4G_user.append(df_max_rrc)
df_zte_4G_user['网元'] = df_zte_4G_user['网元'].astype(int)
df_zte_4G_user = pd.merge(df_zte_4G_user,df_zte_eNodeB,how ='left',on = '网元' )     
