# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 14:49:06 2020

@author: Administrator
"""

import pandas as pd
import os

path = r'C:\Users\Administrator\Desktop\按支局清单'
os.chdir(path)
files = os.listdir(path)

li = []
for file in files:
    df_tmp = pd.read_excel(file,sheet_name = '两周数据对比')
    df_tmp = df_tmp[df_tmp['支局'] != '全县']
    li.append(df_tmp)
df_all = pd.concat(li, axis = 0)
df_all.columns

df_all['用户数变化'] =  df_all['忙时RRC最大连接用户数_本周'] - df_all['忙时RRC最大连接用户数_上周']
df_all['用户数变化率'] =  (df_all['忙时RRC最大连接用户数_本周'] - df_all['忙时RRC最大连接用户数_上周'])/df_all['忙时RRC最大连接用户数_上周']

df_user = df_all[['区县','支局','用户数变化','用户数变化率']]

with pd.ExcelWriter('总表.xlsx') as f:
    df_all.to_excel(f,index =False)

with pd.ExcelWriter('用户数.xlsx') as f:
    df_user.to_excel(f,index =False)