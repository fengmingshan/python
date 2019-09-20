# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 12:50:42 2018

@author: Administrator
"""

import pandas as pd
import os

data_path = r'd:\_3G配置数据汇总' + '\\'
files =  os.listdir(data_path)
df_content = pd.DataFrame()
for file in files:
    if 'BSS' in file:
        df_tmp  = pd.read_excel(data_path  + file ,skiprows = 1, encoding = 'utf-8')
        df_content = df_content.append(df_tmp)
with  pd.ExcelWriter(data_path  + '配置数据汇总.xlsx')  as writer:  #输出到excel
    df_content.to_excel(writer,'配置数据汇总',index = False)


