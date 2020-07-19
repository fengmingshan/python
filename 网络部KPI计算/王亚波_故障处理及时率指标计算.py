# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 08:52:16 2020

@author: Administrator
"""

import pandas as pd
import os

path = r'D:\_python小程序\王亚波KPI指标计算'
os.chdir(path)
df.columns
df = pd.read_excel('报表详单6月.xls',skiprows =2)
df['是否超时'] = df['流程时限'] -  df['有效处理时长(分)']
df['是否超时'] = df['是否超时'].map(lambda x:'否' if x > 0 else '是')

处理及时率 = round(len(df[df['是否超时'] =='否'])/len(df),4)
print('\n')
print(处理及时率)