# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 10:00:46 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
import os


work_path = 'D:/_python小程序/不支持800M终端分析/'
os.chdir(work_path)
df = pd.read_csv('曲靖手机型号库.csv', engine = 'python', encoding  = 'utf-8')
df['号码'] = df['号码'].astype(str)
df['号码'] = df['号码'].map(lambda x:x.split('.')[0])
df['前7位'] = df['号码'].map(lambda x:x[:7])

df_num = pd.read_excel('曲靖号段.xls')
df_num['前7位'] = df_num['前7位'].astype(str)
qj_num = set(list(df_num['前7位']))


df_qj = df[df['前7位'].isin(qj_num)]
df_qj.columns
df_not800 = df_qj[df_qj['是否支持800M'] == '否']

with pd.ExcelWriter('曲靖非800M用户.xlsx') as f:
    df_qj.to_excel(f, '全市用户', index = False)
    df_not800.to_excel(f, '不支持800M用户', index = False)