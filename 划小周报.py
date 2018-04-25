# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 21:44:00 2018
划小周报
@author: Administrator
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import xlsxwriter
from datetime import date

data_path = r'd:\_话务量划小报表\LTE话务数据' + '\\'
out_path = r'd:\_话务量划小报表' + '\\'

os.chdir(data_path) 
all_files = os.listdir() 

for file in all_files:
    df_tmp = pd.read_csv(all_files[0],engine = 'python',skiprows = 5,encoding = 'gbk')
    data = df_tmp.loc[0,'开始时间'].split(' ')[0] 
    
    df_rrc_num = df_tmp[['网元','最大RRC连接用户数_1']]
    df_rrc_num = df_rrc_num.groupby(by='网元',as_index=False)['最大RRC连接用户数_1'].median()
    df_rrc_num['最大RRC连接用户数_1'] = df_rrc_num['最大RRC连接用户数_1'].map(lambda x:int(round(x)))
    
    df_users =  df_tmp[['网元','最大激活用户数_1']]
    df_users =  df_users.groupby(by='网元',as_index=False)[['最大激活用户数_1']].max()
    
    df_throughput =  df_tmp[['网元','空口上行用户面流量（MByte）_1','空口下行用户面流量（MByte）_1477070755617-11']]
    df_throughput['空口上行用户面流量（MByte）_1'] = df_throughput['空口上行用户面流量（MByte）_1'].map(lambda x:float(x.replace(',','')))
    df_throughput['空口下行用户面流量（MByte）_1477070755617-11'] = df_throughput['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:float(x.replace(',','')))
    df_throughput =  df_throughput.groupby(by='网元',as_index=False)[['空口上行用户面流量（MByte）_1'\
                                       ,'空口下行用户面流量（MByte）_1477070755617-11']].sum()
    df_throughput['总流量'] = df_throughput['空口上行用户面流量（MByte）_1'] + df_throughput['空口下行用户面流量（MByte）_1477070755617-11']
    
    df_prb_ratio = df_tmp[['网元','上行PRB平均占用率_1','下行PRB平均占用率_1']]
    df_prb_ratio['上行PRB平均占用率_1'] = df_prb_ratio['上行PRB平均占用率_1'].map(lambda x:float(x.replace('%',''))/100)
    df_prb_ratio['下行PRB平均占用率_1'] = df_prb_ratio['下行PRB平均占用率_1'].map(lambda x:float(x.replace('%',''))/100)
    df_prb_ratio = df_prb_ratio.groupby(by='网元',as_index=False)[['上行PRB平均占用率_1','下行PRB平均占用率_1']].mean()
    
    df_rate =  df_tmp[['网元','分QCI用户体验上行平均速率（Mbps）_1','分QCI用户体验下行平均速率（Mbps）_1']]
    df_rate =  df_rate.groupby(by='网元',as_index=False)[['分QCI用户体验上行平均速率（Mbps）_1','分QCI用户体验下行平均速率（Mbps）_1']].median()
 
    