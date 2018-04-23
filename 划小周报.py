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

data_path = r'd:\_话务量划小报表\LTE话务数据' + '\\'

os.chdir(data_path) 
all_files = os.listdir() 
for file in all_files:
    df_tmp = pd.read_csv(all_files[0],engine = 'python',skiprows = 5,encoding = 'gbk')
    df_rrc_num = df_tmp[['网元','最大RRC连接用户数_1']]
    df_rrc_num = df_rrc_num.groupby(by='网元',as_index=False)['最大RRC连接用户数_1'].median()
    df_rrc_num['最大RRC连接用户数_1'] = df_rrc_num['最大RRC连接用户数_1'].map(lambda x:int(round(x)))    
    df_throughput =  df_tmp[['网元','空口上行用户面流量（MByte）_1','空口下行用户面流量（MByte）_1477070755617-11']]
    df_throughput[['空口上行用户面流量（MByte）_1','空口下行用户面流量（MByte）_1477070755617-11']] = \
    df_throughput[['空口上行用户面流量（MByte）_1','空口下行用户面流量（MByte）_1477070755617-11']].astype(float) 
    df_throughput =  df_throughput.groupby(by='网元',as_index=False)[['空口上行用户面流量（MByte）_1'\
                                       ,'空口下行用户面流量（MByte）_1477070755617-11']].sum()

    