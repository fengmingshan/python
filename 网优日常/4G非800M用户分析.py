# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 13:43:28 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
import os

work_path = 'D:/2020年工作/2020年3月非800M用户分析'
os.chdir(work_path)
df_not_800 = pd.read_excel('./曲靖非800m用户.xlsx')
num1 = set(df_not_800['后面'])

xlsx_file = pd.ExcelFile('./曲靖总流量TOP5小区用户.xlsx')
df_list = []
for name in xlsx_file.sheet_names:
    df_tmp = pd.read_excel('./曲靖总流量TOP5小区用户.xlsx',sheet_name = name)
    df_list.append(df_tmp)
df_resident_cell = pd.concat(df_list, axis = 0)
df_resident_cell.columns
num2 = set(df_resident_cell['号码'])
num1 == num2
