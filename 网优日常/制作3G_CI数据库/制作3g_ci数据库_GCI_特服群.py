# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-20 16:21:24
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-20 16:27:40

import pandas as pd
import os

data_path = 'D:/_python小程序/3GCI数据库制作'

os.chdir(data_path)
gci_files = [x for x in os.listdir('./data/') if 'GCI特服群' in x]
df_gci_special = pd.DataFrame()
for file in gci_files:
    df_tmp = pd.read_excel('./data/' + file)
    df_gci_special = df_gci_special.append(df_tmp)

df_gci_special = df_gci_special[df_gci_special['特服群模板号'] <= 2010]
df_gci_special.rename(columns={'位置区标识 ': '位置区'}, inplace=True)
df_gci_special['全球小区号'] = df_gci_special['全球小区号'].apply(
    lambda x: x.split('(')[1].replace(')', ''))
df_gci_special = df_gci_special[["特服群模板号", "特服用户群",
                                 "特服号码", "号码属性", "用户标识", "区县", "用户别名", "地域", "备份局局向号"]]
with open('./输出/特服群模板.csv', 'w', encoding='utf-8') as writer:  # 输出到excel
    df_gci_special.to_csv(writer, index=False)
