# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 16:50:46 2019

@author: Administrator
"""

import pandas as pd
import os


data_path = r'D:\2019年工作\2019年8月城区20M扩频方案\网管导出15M RRU' + '\\'
out_path =  r'D:\2019年工作\2019年8月城区20M扩频方案' + '\\'

files = os.listdir(data_path)


df_all = pd.DataFrame()
for file  in files :
     df_tmp = pd.read_csv(data_path +file,engine = 'python')
     df_all = df_all.append(df_tmp)

df_res = df_all[df_all['测试结果'] == '1875000kHz']
df_res['eNodeB'] = df_res['网元'].map(lambda x:x.split('=')[2])
df_res['RRU编号'] = df_res['测试对象'].map(lambda x:x.split('(')[2].split(',')[0])
df_res.drop_duplicates(['网元名称','测试对象'],keep='first', inplace = True)
df_res['RRU编号'] = df_res['RRU编号'].astype(int)
df_res['小区编号'] = df_res['RRU编号'] - 50


with pd.ExcelWriter(out_path + '15M_RRU配置信息.xlsx') as writer:
     df_res.to_excel(writer,'15M_RRU',index = False )

