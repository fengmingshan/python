# -*- coding: utf-8 -*-
# @Author: Administrator


import pandas as pd
import os

data_path = 'D:/_python小程序/3GCI数据库制作'

os.chdir(data_path)
hw_files = [x for x in os.listdir('./data/') if 'CDMA小区报表' in x]
df_hw = pd.DataFrame()
for file in hw_files:
    df_tmp = pd.read_csv('./data/' + file,engine ='python',encoding = 'gbk')
    df_hw = df_hw.append(df_tmp)
df_hw.columns
df_hw = df_hw[df_hw['小区识别码']!= '-']


df_hw['全球小区号'] = df_hw['小区识别码'].map(lambda x:eval('0x' + x.replace('H','').replace('00','')))
df_hw['区县'] = df_hw['基站名称'].map(lambda x:x.split('QJ')[1][:2])

df_hw = df_hw[['区县',"CBSC名称", "基站名称", "位置区码", "小区识别码",'全球小区号']]

with open('./输出/华为小区.csv', 'w', encoding='utf-8',newline = '') as writer:  # 输出到excel
    df_hw.to_csv(writer, index=False)
