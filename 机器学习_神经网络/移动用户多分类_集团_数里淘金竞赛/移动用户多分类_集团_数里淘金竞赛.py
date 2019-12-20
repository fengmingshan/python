# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:41:10 2019

@author: Administrator
"""
import pandas as pd
import os
import pandas_profiling

work_path = 'D:/2019年工作/2019年12月集团_数里淘金竞赛_移动用户多分类'
os.chdir(work_path)

file_list = os.listdir('.')

# 读取数据
df_call = pd.read_csv('./data/call_data.csv',engine = 'python',encoding = 'utf-8')
df_consumer = pd.read_csv('./data/cust_data.csv',engine = 'python',encoding = 'utf-8')
df_dpi = pd.read_csv('./data/dpi_data.csv',engine = 'python',encoding = 'utf-8')
df_period = pd.read_csv('./data/prd_data.csv',engine = 'python',encoding = 'utf-8')
df_terminal = pd.read_csv('./data/trmnl_data.csv',engine = 'python',encoding = 'utf-8')

df = pd.merge(df_call,df_consumer,how = 'left' , on = 'user' )
df = pd.merge(df,df_dpi,how = 'left' , on = 'user' )
df = pd.merge(df,df_period,how = 'left' , on = 'user' )
df = pd.merge(df,df_terminal,how = 'left' , on = 'user' )

df = pd.read_csv('用户数据_合.csv',engine = 'python')

df_feature = df.isnull().any()
df_null = df_feature[df_feature==True]
null_feature = list(df_null.index)