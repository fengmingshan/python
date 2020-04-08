# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:09:14 2020

@author: Administrator
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import csv
import os

work_path = 'D:\_python小程序\MR报表\原始数据'
os.chdir(work_path)
all_files = os.listdir(work_path)
summary_files = [x for x in all_files if '总表' in x]
detail_files = [x for x in all_files if '详表' in x]

# 处理总表
summary_list = []
for file in summary_files:
    df_tmp = pd.read_csv(file, sep = ',', engine = 'python')
    df_list.append(df_tmp)
df_summary = pd.concat(summary_list, axis = 0)
df_summary.reset_index(drop=True, inplace=True)
df_summary.rename(columns = {'区域':'area',
                             '时间周期':'date',
                             '扇区数量':'cell_num',
                             '是否800M设备':'is_800',
                             '|≥-105dBm比例':'above-105',
                             '|-110<=RSRP<-105dBm比例':'-110to-105',
                             '-115<=RSRP<-110dBm比例':'-115to-110',
                             '|-120<=RSRP<-115dBm比例':'-120to-115',
                             '|≥负无穷比例':'inf'
                             },inplace = True)
df_summary['date'] = pd.to_datetime(df_summary['date'])
df_summary['date'] = df_summary['date'].map(lambda x:str(x).split(' ')[0])

df_summary['mr_good'] = df_summary['above-105'] + df_summary['-110to-105']
df_summary['primary_key'] = df_summary['area'] + '_' +  df_summary['date']

# 处理详表
col = ['区域','时间周期','NAME','厂家','是否800M设备','平均RSRP（dBm）','|≥-105dBm采样点','|≥-110dBm采样点','|≥-115dBm采样点','|≥-120dBm采样点','|≥负无穷采样点']
detail_list = []
for file in detail_files:
    with open(file,'r',newline ='')as f:
        reader = csv.reader(f,delimiter =',')
        rows = [x[0:2] + [','.join(x[2:-8])] + x[-8:] for x in reader]
        df_tmp = pd.DataFrame (rows[1:],columns = col)
        df_tmp = df_tmp[df_tmp['区域']=='曲靖市']
        detail_list.append(df_tmp)
df_detail = pd.concat(detail_list, axis = 0)
df_detail.reset_index(drop=True, inplace=True)
df_detail.rename(columns = {'区域':'area',
                             '时间周期':'date',
                             '厂家':'factory',
                             '是否800M设备':'is_800',
                             '平均RSRP（dBm）':'avg_rsrp',
                             '|≥-105dBm采样点':'above-105',
                             '|≥-110dBm采样点':'-110to-105',
                             '|≥-115dBm采样点':'-115to-110',
                             '|≥-120dBm采样点':'-120to-115',
                             '|≥负无穷采样点':'inf'
                             },inplace = True)
df_detail['date'] = pd.to_datetime(df_detail['date'])
df_detail['date'] = df_detail['date'].map(lambda x:str(x).split(' ')[0])
df_detail['avg_rsrp'] = df_detail['avg_rsrp'].astype(float)
for col in ['above-105', '-110to-105', '115to-110', '-120to-115', 'inf']:
    df_detail[col] = df_detail[col].astype(int)
df_detail['mr_good'] = df_detail['above-105'] + df_detail['-110to-105']
df_detail['primary_key'] = df_detail['NAME'] + '_' +  df_detail['date']

# 数据入库
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@localhost:3306/eric_traffic?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
