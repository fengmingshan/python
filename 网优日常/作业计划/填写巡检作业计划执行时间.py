# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 09:23:47 2019

@author: Administrator
"""
import datetime
from datetime import datetime
import pandas as pd
from pandas import DataFrame
import numpy as np
import os
import math

path = 'D:\Test\填写作业计划'
os.chdir(path)
date_file = '日期.xlsx'
bts_file = '全量站址.xlsx'

df_bts = pd.read_excel(bts_file)

df_date = pd.read_excel(date_file)


df_date['month'] = df_date['日期'].map(lambda x:str(x).split('-')[1])
df_date['日期'] = df_date['日期'].apply(lambda x:str(x).split(' ')[0])

df_res = pd.DataFrame()
df_date1 =  df_date[df_date['month'].isin(['01','02','03'])]
quxian_list = list(set(df_bts['区县']))
for quxian in quxian_list:
    df_tmp = df_bts[df_bts['区县']== quxian]
    df_tmp.reset_index(inplace = True)
    n = math.ceil(len(df_tmp)/len(df_date1))
    for i in range(len(df_date1)):
        for j in range(n):
            if (i+j*len(df_date1)) < len(df_tmp):
                df_tmp.loc[(i+j*len(df_date1)),'巡检日期1'] = df_date1.loc[i,'日期']
            else:
                pass
    print('finish:',quxian)
    df_res = df_res.append(df_tmp)

with pd.ExcelWriter('结果.xlsx') as  writer:
     df_res.to_excel(writer,index = False)

