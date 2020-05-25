# -*- coding: utf-8 -*-
# @Author: Administrator


import pandas as pd
import os

data_path = 'D:/_python小程序/3GCI数据库制作'

os.chdir(data_path)
hw_files = [x for x in os.listdir('./data/') if '华为' in x]
df_hw = pd.DataFrame()
for file in hw_files:
    df_tmp = pd.read_excel('./data/' + file)
    df_hw = df_hw.append(df_tmp)

df_hw = df_hw[["区县", "BBU名称", "基站名", "TRM描述信息", "全球小区号"]]
with open('./输出/华为小区.csv', 'w', encoding='utf-8',newline = '') as writer:  # 输出到excel
    df_hw.to_csv(writer, index=False)
