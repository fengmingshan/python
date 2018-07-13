# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 16:22:06 2018

@author: Administrator
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import xlsxwriter
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

# =============================================================================
# 环境变量
# =============================================================================
data_path = r'd:\_感知质差小区分析' + '\\'
traffic_path = r'd:\_感知质差小区分析\traffic' + '\\'
prb_path = r'd:\_感知质差小区分析\prb' + '\\'

pic_path = r'd:\_感知质差小区分析\pic' + '\\'

df_traffic_title  = pd.read_excel(data_path + 'traffic_title.xlsx',encoding = 'utf-8')
traffic_title = list(df_traffic_title.columns)
df_prb_title  = pd.read_excel(data_path + 'prb_title.xlsx',encoding = 'utf-8')
prb_title = list(df_prb_title.columns)




traffic_files = os.listdir(traffic_path) 
prb_files = os.listdir(prb_path) 


file = '0611-0618.csv'
for file in traffic_files:    
    df_tmp = pd.read_csv(traffic_path + file,header = None,names = traffic_title, engine = 'python', encoding = 'gbk')
    df_tmp['DATE_ID'] = df_tmp['DATE_ID'].map(lambda x:x.replace('\'',''))
    df_tmp['eNodeB'] = df_tmp['eNodeB'].map(lambda x:x.replace('\'',''))
    date = df_tmp.loc[0,'DATE_ID']
    
    # =============================================================================
    # 计算每日实际忙时确定RRC连接用户数
    # =============================================================================
    df_pivot_rrc = pd.pivot_table(df_tmp, index=['HOUR_ID'], values = 'Max number of UE in RRc', aggfunc = {'Max number of UE in RRc':np.sum})                                                  
    df_pivot_rrc = df_pivot_rrc.sort_values(by='Max number of UE in RRc',ascending = False)
    df_pivot_rrc = df_pivot_rrc.reset_index()
    busy_hour =  df_pivot_rrc.loc[0,'HOUR_ID']
    df_max_rrc =  df_tmp[['eNodeB','Max number of UE in RRc']][df_tmp['HOUR_ID'] == busy_hour]
    
    df_pivot = pd.pivot_table(df_tmp, index=['eNodeB'],
                              values = ['Air Interface_Traffic_Volume_UL_MBytes',
                                        'Air Interface_Traffic_Volume_DL_MBytes'], 
                              aggfunc = {'Air Interface_Traffic_Volume_UL_MBytes':np.sum,
                                         'Air Interface_Traffic_Volume_DL_MBytes':np.sum})  
    df_pivot['总流量'] = df_pivot['Air Interface_Traffic_Volume_UL_MBytes'] + df_pivot['Air Interface_Traffic_Volume_DL_MBytes']
    df_pivot = df_pivot.reset_index()
    df_pivot = pd.merge(df_pivot,df_max_rrc,on = 'eNodeB',how = 'left')  
    df_pivot['日期'] = date.replace('-','/')
    df_pivot.rename(columns={'eNodeB':'网元',
                             'Max number of UE in RRc' : 'RRC连接用户数',
                             'Air Interface_Traffic_Volume_UL_MBytes':'上行流量(MB)',
                             'Air Interface_Traffic_Volume_DL_MBytes':'下行流量(MB)'},inplace =True)
    df_combine = df_combine.append(df_pivot)  

