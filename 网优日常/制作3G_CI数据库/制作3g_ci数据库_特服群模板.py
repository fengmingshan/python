# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-20 16:21:24
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-20 16:27:40

import pandas as pd
import os

data_path = 'D:/_python小程序/3GCI数据库制作'

os.chdir(data_path)
gci_files = [x for x in os.listdir('./data/') if '特服群模板' in x]
df_template = pd.DataFrame()
for file in gci_files:
    df_tmp = pd.read_excel('./data/' + file)
    df_template = df_template.append(df_tmp)

df_template.rename(columns = {'特服群模板编号 ':'特服群模板号'},inplace=True)
df_template = df_template[(df_template['特服用户群'] == 110)&(df_template['特服群模板号'] <= 2010)]
df_template['用户标识'] = df_template['用户标识'].apply(
    lambda x: x.replace('--','——'))
df_template['区县'] = df_template['用户标识'].apply(
    lambda x: x.split('——')[1][:2])
df_template['区县'] = df_template['区县'].apply(
    lambda x: x.replace('西片','麒麟'))

df_template = df_template[["特服群模板号", "特服用户群", "特服号码", "号码属性", "用户标识", "区县", "用户别名", "地域", "备份局局向号"]]
with open('./输出/特服群模板.csv', 'w', encoding='utf-8',newline = '') as writer:  # 输出到excel
    df_template.to_csv(writer, index=False)
