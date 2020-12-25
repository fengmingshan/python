# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 09:43:33 2020

@author: Administrator
"""

import pandas as pd
import os

path = r'C:\Users\Administrator\Desktop\3G历史告警'
os.chdir(path)

files = os.listdir()

li1 = []
for f in files:
    df = pd.read_excel(f, encoding = 'gbk')
    li1.append(df)

df_3g = pd.concat(li1,axis = 0)
df_3g.告警对象.head(50)
df_3g.columns
及时率 = len(df_3g['编号'][df_3g['持续时间']<=5760])/len(df_3g['编号'])
