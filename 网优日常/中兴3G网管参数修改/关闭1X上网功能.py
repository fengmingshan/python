# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:27:13 2019

@author: Administrator
"""

import pandas as pd
import os

# 申请权限
# APPLY CMRIGHT:SYSTEM=102;

# 关闭1X上网
# SET 1X_CELL:POS="1"-"0",SERVICERESTRICTMODE=2;

# 修改载频功率脚本

# =============================================================================
# 设置环境变量
# =============================================================================
data_path = 'd:/test/关闭1X上网功能'
os.chdir(data_path)
files = os.listdir('./')
forbid_list = ['105','119','16','169','326','373','405','408','76','9']
li = []
for file in files:
    df_tmp = pd.read_excel(file,skiprows =3)
    li.append(df_tmp)
df_cell_info = pd.concat(li,axis =0)

df_cell_info = df_cell_info[df_cell_info['前向功率不足导致的拥塞'] > 10]

df_cell_info['BTS_no'] = df_cell_info['BTS'].map(lambda x:x.split(' ')[0])
df_cell_info['cell_info'] = df_cell_info['BTS_no'].map(str) +'_'+ df_cell_info['Cell'].map(str)

df_cell_info.drop_duplicates('cell_info',keep ='first',inplace =True)
df_cell_info = df_cell_info[~df_cell_info['BTS_no'].isin(forbid_list)]
df_cell_info.reset_index(drop =True,inplace =True)

# 参数修改脚本
with open('./关闭1X上网.txt', 'w') as f:
    for i in range(0, len(df_cell_info), 1):
        line1 = 'APPLY CMRIGHT:SYSTEM={bts};'\
        .format(bts = df_cell_info.loc[i, 'BTS_no'])
        line2 = 'SET 1X_CELL:POS="{bts}"-"{cell}",SERVICERESTRICTMODE=2;'\
        .format(bts = df_cell_info.loc[i, 'BTS_no'],
             cell = df_cell_info.loc[i, 'Cell'])
        f.write(line1+'\n')
        f.write(line2+'\n')

