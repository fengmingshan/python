# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 09:28:00 2019

@author: Administrator
"""
import pandas as pd
import os

data_path = r'D:\2019年工作\2019年8月4G网络扩频方案\诺基亚大数据平台' + '\\'
file = 'qujing_rmk1_20190802.csv'

bts_info_path = r'd:\2019年工作\2019年8月4G网络扩频方案\基站信息表'  + '\\'
L1800_info = 'L1800_info.xlsx'
L800_info = 'L800_info.xlsx'

df_L1800 = pd.read_excel(bts_info_path + L1800_info,encoding = 'utf-8')
df_L800 = pd.read_excel(bts_info_path + L800_info,encoding = 'utf-8')


df_town = df_L1800.append(df_L800)[['eNodeB','town']]
df_town.drop_duplicates('eNodeB', keep='first', inplace = True)
df_town.set_index('eNodeB', inplace = True)
town_dict = df_town.to_dict()

df_net_type = df_L1800.append(df_L800)[['eNodeB','net_type']]
df_net_type.drop_duplicates('eNodeB', keep='first', inplace = True)
df_net_type.set_index('eNodeB', inplace = True)
net_type_dict = df_net_type.to_dict()

user_data = pd.read_csv(data_path + file,engine = 'python',encoding = 'utf-8',  chunksize = 10000)
for df_tmp in user_data:





