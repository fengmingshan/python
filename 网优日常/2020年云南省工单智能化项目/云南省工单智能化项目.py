# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 17:28:22 2020

@author: Administrator
"""
import pandas as pd
import os

work_path = r'D:\2020年工作\2020年工单智能化项目'
os.chdir(work_path)
files = os.listdir(work_path)
files
df_power = pd.read_csv('动环故障.csv',encoding ='gbk')
df_other = pd.read_csv('其他类.csv',encoding ='gbk')

df_power.head(10)
df_power.OPER_DETAIL.head(5)