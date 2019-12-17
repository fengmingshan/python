# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:41:10 2019

@author: Administrator
"""
import pandas as pd
import os
import pandas_profiling

work_path = 'D:/_python/python/机器学习_神经网络/移动用户多分类_集团_数里淘金竞赛'
os.chdir(work_path)

file_list = os.listdir('./data')

# 数据清洗
df_call = pd.read_csv('./data/call_data.csv',engine = 'python',encoding = 'utf-8')
df_consumer = pd.read_csv('./data/cust_data.csv',engine = 'python',encoding = 'utf-8')
df_dpi = pd.read_csv('./data/dpi_data.csv',engine = 'python',encoding = 'utf-8')
df_period = pd.read_csv('./data/prd_data.csv',engine = 'python',encoding = 'utf-8')
df_terminal = pd.read_csv('./data/trmnl_data.csv',engine = 'python',encoding = 'utf-8')

df = pd.merge(df_call,df_consumer,how = 'left' , on = 'user' )
df = pd.merge(df,df_dpi,how = 'left' , on = 'user' )
df = pd.merge(df,df_period,how = 'left' , on = 'user' )
df = pd.merge(df,df_terminal,how = 'left' , on = 'user' )

with open('用户数据_合.csv','w') as f:
    df.to_csv(f,index = False)
