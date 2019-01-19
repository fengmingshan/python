# -*- coding: utf-8 -*-
"""
Created on Wed May  9 16:49:51 2018
汇总性能数据15分钟
@author: Administrator
"""

import pandas as pd
import numpy as np
import os

data_path = r'd:\test\LTE' + '\\'
file_list = os.listdir(data_path)

df_combine = pd.DataFrame()

for file in file_list:
    df_tmp = pd.read_csv(data_path + file,skiprows = 5,engine = 'python', encoding = 'gbk')
    df_combine = df_combine.append(df_tmp) 

df_pivot = pd.pivot_table(df_combine, index=['网元'],
                          values = ['平均RRC连接用户数_1',
                                    '下行平均激活用户数_1',
                                    '下行PRB平均占用率_1',
                                    '分QCI用户体验下行平均速率（Mbps）_1'],                                   
                          aggfunc = {'平均RRC连接用户数_1':np.max,
                                     '下行平均激活用户数_1':np.max,
                                     '下行PRB平均占用率_1':np.max,
                                     '分QCI用户体验下行平均速率（Mbps）_1':np.max})    

with pd.ExcelWriter(data_path + 'prb.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_pivot.to_excel(writer,'prb') 
