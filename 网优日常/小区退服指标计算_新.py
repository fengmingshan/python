# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:39:32 2019

@author: Administrator
"""

import pandas as pd 
import os
from datetime import datetime 
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

current_date = str(datetime.now()).split('.')[0].split(' ')[0]

data_path = r'D:\2019年工作\2019年4月小区退服指标计算（新）' + '\\'
pic_path = r'D:\2019年工作\2019年4月小区退服指标计算（新）\PIC' + '\\'

all_files = os.listdir(data_path)
files = [x for x in all_files if 'alarm_cel_exit_service_child' in x] 

df_原始数据 = pd.DataFrame()
for file in files :
    df_tmp = pd.read_excel(data_path + file,skiprows = 1)
    df_原始数据 = df_原始数据.append(df_tmp)



# =============================================================================
# 计算各县累计断站时长
# =============================================================================

with  pd.ExcelWriter(data_path + '断站原始数据.xlsx')  as writer:  #输出到excel
    df_原始数据.to_excel(writer,'断站原始数据',index=False) 

    
