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

df_zte_eNodeB =  pd.read_excel(data_path + 'zte_eNode_name.xls',encoding = 'utf-8')

files_3G = os.listdir(path_3g) 
files_3G_busy = os.listdir(path_3g_busy) 


df_zte_3G_traffic = pd.DataFrame()
for file in files_3G:    
    df_tmp = pd.read_csv(path_3g + file,engine = 'python', encoding = 'gbk')
    df_tmp.fillna(0,inplace=True)
    df_tmp.columns = df_tmp.columns.map(lambda x:x.strip())
    df_tmp['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y-%m-%d")  
    week = str(df_tmp.iloc[0,0]).split(' ')[0][5:10] + "_" + str(df_tmp.iloc[-1,0]).split(' ')[0][5:10]
    df_tmp['week'] = week
    df_zte_3G_traffic = df_zte_3G_traffic.append(df_tmp)

df_zte_3G_traffic['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y-%m-%d")  
df_zte_3G_traffic.rename(columns={'DO: 小区RLP信息对象.前向MacIndex最大忙数':'3G用户数',
                                  'DO: 小区RLP信息对象.RLP层前向传送字节数(KB)':'3G流量(GB)',
                                  '1X: 小区CS呼叫话务量(Erl)':'1X话务量',
                                  'Cell':'网元'},inplace =True)
df_zte_3G_traffic['3G流量(GB)'] =  df_zte_3G_traffic['3G流量(GB)'].map(lambda x:x.replace('-','0'))
df_zte_3G_traffic['3G用户数'] =  df_zte_3G_traffic['3G用户数'].map(lambda x:x.replace('-','0'))
df_zte_3G_traffic['3G流量(GB)'] =  df_zte_3G_traffic['3G流量(GB)'].astype(float) 
df_zte_3G_traffic['3G流量(GB)'] =  df_zte_3G_traffic['3G流量(GB)']/(1024*1024)
df_zte_3G_traffic['网元'] =  df_zte_3G_traffic['网元'].map(lambda x:x.split('_')[2])
df_zte_3G_traffic['网元'] =  df_zte_3G_traffic['网元'].map(lambda x:x.split('J')[1])

df_zte_3G_traffic =  df_zte_3G_traffic[['week','网元','1X话务量','3G流量(GB)']]
df_zte_3G_traffic = pd.pivot_table(df_zte_3G_traffic, index=['week','网元'], 
                                   values = ['1X话务量','3G流量(GB)'], 
                                   aggfunc = {'1X话务量':np.sum,'3G流量(GB)':np.sum})  
df_zte_3G_traffic = df_zte_3G_traffic.reset_index()                                                     

df_zte_3G_traffic = pd.merge(df_zte_3G_traffic,df_zte_eNodeB,how ='left',on = '网元' )     

df_zte_3G_user = pd.DataFrame()
for file in files_3G_busy:    
    df_tmp = pd.read_csv(path_3g_busy + file,engine = 'python', encoding = 'gbk')
    df_tmp.fillna(0,inplace=True)
    df_tmp.columns = df_tmp.columns.map(lambda x:x.strip())
    df_tmp['开始时间'] = pd.to_datetime(df_tmp['开始时间'],format="%Y-%m-%d")  
    df_tmp.rename(columns={'1X: Sector基本性能测量对象.定时登记成功次数':'1X用户数',
                           'Cell':'网元'},inplace =True)
    df_tmp['网元'] =  df_tmp['网元'].map(lambda x:x.split('_')[2])
    df_tmp['网元'] =  df_tmp['网元'].map(lambda x:x.split('J')[1])
    week = str(df_tmp.iloc[0,0]).split(' ')[0][5:10] + "_" + str(df_tmp.iloc[-1,0]).split(' ')[0][5:10]
    df_tmp['week'] = week
    # =============================================================================
    # 计算每日实际忙时确定RRC连接用户数
    # =============================================================================
    df_pivot_1Xuser = pd.pivot_table(df_tmp, index=['开始时间'], values = '1X用户数', aggfunc = {'1X用户数':np.sum})                                                  
    df_pivot_1Xuser = df_pivot_1Xuser.sort_values(by='1X用户数',ascending = False)
    df_pivot_1Xuser = df_pivot_1Xuser.reset_index()
    busy_hour =  df_pivot_1Xuser.loc[0,'开始时间']
    df_max_user =  df_tmp[['开始时间','week','网元','1X用户数']][df_tmp['开始时间'] == busy_hour]    
    df_max_user =  df_max_user[['week','网元','1X用户数']]
    df_zte_3G_user = df_zte_3G_user.append(df_max_user)
df_zte_3G_user = pd.merge(df_max_user,df_zte_eNodeB,how ='left',on = '网元' )     


with  pd.ExcelWriter(out_path + 'df_zte_3G_traffic.xlsx')  as writer:  #输出到excel
    df_tmp.to_excel(writer, 'df_zte_3G_traffic') 
        
