# -*- coding: utf-8 -*-
"""
Created on Wed May  9 16:49:51 2018
汇总性能数据15分钟
@author: Administrator
"""

import pandas as pd
import os

data_path = r'd:\2018年工作\2018年5月LTE负荷优化\扇区忙时' + '\\'
file_list = os.listdir(data_path)

df_combine = pd.DataFrame()

for file in file_list:
    df_tmp = pd.read_excel(data_path + file, encoding='utf-8') 
    df_combine = df_combine.append(df_tmp) 
